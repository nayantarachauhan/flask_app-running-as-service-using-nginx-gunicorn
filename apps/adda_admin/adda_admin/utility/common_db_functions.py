# from flask_restful import reqparse
# from adda_api import *
# from sqlalchemy import func



# class DB_query:
    
#     def get(table):
#         parser = reqparse.RequestParser()
#         parser.add_argument('ref_num', type=str, help='ref_num is needed!', required = True)
#         parser.add_argument('source_name', type=str, help='source_name is needed!', required = True)
#         args = parser.parse_args()
#         results = db.session.query(table).filter(table.ref_num == args['ref_num'], table.source_name == args['source_name'])
#         return results

    
#     def getFromVehicle(table, status):
#         parser = reqparse.RequestParser()
#         parser.add_argument('source_name', type=str, help='source_name is needed!', required = True)
#         parser.add_argument('start_date', type=str)
#         parser.add_argument('stop_date', type=str)
#         args = parser.parse_args()

#         if args['start_date'] is None and args['stop_date'] is None:
#             results = db.session.query(table).filter(table.source_name == args['source_name'], table.claim_state == status)
        
#         elif args['stop_date'] is None:
#             results = db.session.query(table).filter(table.source_name == args['source_name'], table.claim_state == status, table.created_at >= args['start_date'])

#         else:
#             results = db.session.query(table).filter(table.source_name == args['source_name'], table.claim_state == status, table.created_at >= args['start_date'],  table.created_at <= args['stop_date'] )

#         return results

    

#     def getAssessReport(table):
#         parser = reqparse.RequestParser()
#         parser.add_argument('source_name', type=str, help='source_name is needed!', required = True)
#         parser.add_argument('start_date', type=str)
#         parser.add_argument('stop_date', type=str)
#         args = parser.parse_args()

#         if args['start_date'] is None and args['stop_date'] is None:
#             results = db.session.query(func.sum(table.total_claims), func.sum(table.completed), func.sum(table.failed) ).filter(table.source_name == args['source_name']).order_by(table.created_at.desc())
        
#         elif args['stop_date'] is None:
#             results = db.session.query(func.sum(table.total_claims), func.sum(table.completed), func.sum(table.failed)).filter(table.source_name == args['source_name'], table.created_at >= args['start_date'])

#         else:
#             results = db.session.query(func.sum(table.total_claims), func.sum(table.completed), func.sum(table.failed)).filter(table.source_name == args['source_name'], table.created_at >= args['start_date'],  table.created_at <= args['stop_date'] )

#         return results

    

#     def put(_id, table):
#         parser = reqparse.RequestParser()
#         parser.add_argument('column_name', type=str, help='column_name is needed!', required = True)
#         parser.add_argument('column_value', type=str, help='column_value is needed!', required = True)
#         args = parser.parse_args()

#         db.session.query(table).filter_by(id = _id).update({args["column_name"]: args['column_value']})
        
#         db.session.commit()

    

#     def delete(table):
#         parser = reqparse.RequestParser()
#         parser.add_argument('ref_num', type=str, help='ref_num is needed!', required = True)
#         parser.add_argument('source_name', type=str, help='source_name is needed!', required = True)
#         args = parser.parse_args()

#         db.session.query(table).filter(table.ref_num == args['ref_num'], table.source_name == args['source_name']).delete(synchronize_session=False)
#         db.session.commit()
