The project involves the creation of a Vendor Management System with Performance metrics.

Technologies used involve: 
1. Django - for backend
2. Postgres - for the database
3. Docker
4. Git

Testing using Curl:

1. To change status of a purchase order from PENDING to complete, use: curl -X POST http://0.0.0.0:8000/api/purchase-orders/<int:number>/mark_completed/ - where replace the <int:number> with the purchase order id.

2. To check the updation of quality rating average of a vendor, use: curl -X POST http://0.0.0.0:8000/api/vendors/update_quality_rating_avg/ -d "vendor_id=5" - where you can replace the vendor_id with any other existing vendor id in the database.

