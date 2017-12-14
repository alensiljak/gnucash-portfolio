"""
Accounts business layer
"""
from typing import List
from piecash import Book, Account

def get_account_id_by_fullname(book: Book, fullname: str) -> str:
    """ Locates the account by fullname """
    # get all accounts and iterate, comparing the fullname. :S
    query = (
        book.session.query(Account)
    )
    #sql = str(query.statement.compile(dialect=sqlite.dialect(), compile_kwargs={"literal_binds": True}))
    #print(sql)
    all_accounts = query.all()
    for account in all_accounts:
        if account.fullname == fullname:
            return account.guid


def get_all_child_accounts_as_array(account: Account) -> List[Account]:
    """ Returns all child accounts in a list """
    result = []
    # ignore placeholders
    if not account.placeholder:
        #continue
        result.append(account)

    for child in account.children:
        sub_accounts = get_all_child_accounts_as_array(child)
        result += sub_accounts

    return result


def test():
    """ run tests """
    print("sorry, nothing to see here yet")


######################################
if __name__ == "__main__":
    test()
