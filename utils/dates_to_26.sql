/*
	This script migrates the date formats between GnuCash versions 2.6 and 2.7.
	Version 2.6 stores dates in YYYYMMDDHHmmss format, while
	version 2.7 stores dates in YYYY-MM-DD HH:mm:ss format.

	To run, first test and then replace the 'rollback' statement at the end with 'commit'.
*/

/*
-- Sample statement for migration to 2.7:
select post_date, substr(post_date, 0, 5) || '-' || substr(post_date, 5, 2) || '-' || substr(post_date, 7, 2) 
	|| " " || substr(post_date, 9, 2) || ":" || substr(post_date, 11, 2) || ":" || substr(post_date, 13,2) as newdate
from transactions
where length(post_date) = 14

-- Sample statement for migration back to 2.6:
select post_date, 
	substr(post_date, 0, 5) || substr(post_date, 6, 2) || substr(post_date, 9, 2) 
	|| substr(post_date, 12, 2) || substr(post_date, 15, 2) || substr(post_date, 18,2) as olddate
from transactions
where length(post_date) = 19
*/

-- Splits, reconcile_date
begin transaction;

-- Splits: reconcile_date
update splits
set reconcile_date = substr(reconcile_date, 0, 5) || substr(reconcile_date, 6, 2) || substr(reconcile_date, 9, 2) 
	|| substr(reconcile_date, 12, 2) || substr(reconcile_date, 15, 2) || substr(reconcile_date, 18,2)
where length(reconcile_date) = 19;

-- Transactions: post_date, enter_date
update transactions
set enter_date = substr(enter_date, 0, 5) || substr(enter_date, 6, 2) || substr(enter_date, 9, 2) 
	|| substr(enter_date, 12, 2) || substr(enter_date, 15, 2) || substr(enter_date, 18,2)
where length(enter_date) = 19;

update transactions
set post_date = substr(post_date, 0, 5) || substr(post_date, 6, 2) || substr(post_date, 9, 2) 
	|| substr(post_date, 12, 2) || substr(post_date, 15, 2) || substr(post_date, 18,2)
where length(post_date) = 19;

-- Prices: [date]
update Prices
set date = substr(date, 0, 5) || substr(date, 6, 2) || substr(date, 9, 2) 
	|| substr(date, 12, 2) || substr(date, 15, 2) || substr(date, 18,2)
where length(date) = 19;
rollback;
