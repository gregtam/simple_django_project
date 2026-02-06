import os
from datetime import date, timedelta
import time

from celery import shared_task
from dotenv import load_dotenv
import pandas as pd
import plaid
from plaid.api import plaid_api
from plaid.model.products import Products
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
import json


@shared_task
def simple_sleep_task():
    print(f"Starting task, will sleep for 5 seconds")
    time.sleep(5)
    print(f"Task complete!")


@shared_task
def run_plaid_sandbox_test():
    try:
        load_dotenv()

        # 1. Initialize Plaid Client
        configuration = plaid.Configuration(
            host=plaid.Environment.Sandbox,
            api_key={
                'clientId': os.getenv('PLAID_CLIENT_ID'),
                'secret': os.getenv('PLAID_SANDBOX_SECRET'),
            }
        )
        api_client = plaid.ApiClient(configuration)
        client = plaid_api.PlaidApi(api_client)

        # 2. Generate a Sandbox Public Token (Bypasses the Frontend UI)
        # 'ins_109' is the ID for "First Platypus Bank" (The standard test bank)
        sandbox_req = SandboxPublicTokenCreateRequest(
            institution_id='ins_5',
            initial_products=[Products('transactions')]
        )
        sandbox_res = client.sandbox_public_token_create(sandbox_req)
        public_token = sandbox_res['public_token']
        print(f"Generated Public Token: {public_token}")

        # 3. Exchange Public Token for Access Token
        exchange_req = ItemPublicTokenExchangeRequest(public_token=public_token)
        exchange_res = client.item_public_token_exchange(exchange_req)
        access_token = exchange_res['access_token']
        print(f"Exchanged Access Token: {access_token}")

        time.sleep(10)

        # 4. Use Access Token to Fetch Transactions with retry logic
        # Fetching the last 30 days of data
        start_date = date.today() - timedelta(days=30)
        end_date = date.today()

        # Keep waiting until the product is ready
        while True:
            try:
                trans_req = TransactionsGetRequest(
                    access_token=access_token,
                    start_date=start_date,
                    end_date=end_date
                )
                trans_res = client.transactions_get(trans_req)
                break  # Success, exit loop
            except plaid.ApiException as retry_error:
                error_body = json.loads(retry_error.body) if isinstance(retry_error.body, str) else retry_error.body
                error_code = error_body.get('error_code', '')

                if error_code == 'PRODUCT_NOT_READY':
                    time.sleep(1)
                else:
                    # Different error, don't retry
                    raise

        transactions_df = pd.DataFrame([
            {k: d[k] for k in ['account_id', 'transaction_id', 'date', 'amount', 'name']}
            for d in trans_res['transactions']
        ]).rename({'name': 'transaction_name'}, axis=1)

        accounts_df = pd.DataFrame([
            {k: d[k] for k in ['account_id', 'name', 'official_name']}
            for d in trans_res['accounts']
        ]).rename({'name': 'account_name'}, axis=1)

        transactions_summary_df = transactions_df.merge(
            accounts_df, on='account_id', how='left'
        )

        return transactions_summary_df.to_dict('records')

    except plaid.ApiException as e:
        print(f"Plaid API Error: {e.body}")
        # Return empty list instead of None so view doesn't fail
        return []


@shared_task
def sync_plaid_transactions_for_all_users():
    """Periodic task to sync Plaid transactions for all users"""
    from django.contrib.auth import get_user_model
    from transactions.models import PlaidTransactionsModel
    from datetime import datetime

    User = get_user_model()
    users = User.objects.all()

    total_synced = 0
    for user in users:
        try:
            # Run sandbox test to get new transactions
            transactions = run_plaid_sandbox_test()

            # Save to database
            for transaction in transactions:
                date_value = transaction['date']
                if isinstance(date_value, str):
                    date_value = datetime.strptime(date_value, '%Y-%m-%d').date()

                PlaidTransactionsModel.objects.update_or_create(
                    user_uuid=user.uuid,
                    transaction_id=transaction['transaction_id'],
                    defaults={
                        'date': date_value,
                        'amount': transaction['amount'],
                        'transaction_name': transaction['transaction_name'],
                        'account_name': transaction['account_name'],
                        'account_id': transaction.get('account_id', ''),
                    }
                )

        except Exception as e:
            print(f"Error syncing transactions for user {user.uuid}: {e}")

    print(f"Total transactions synced: {total_synced}")
    return total_synced