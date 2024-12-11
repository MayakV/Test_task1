from flask import Flask
from flask_restx import Api, Resource, reqparse

from utils import bq_api


app = Flask(__name__)
api = Api(app, title="Test API", default="BigQuery dataset", default_label="")


@api.route('/persons_per_date/<last_dates_count>', methods=['GET'])
@api.doc(description="The endpoint to retrieve the number of distinct persons per date "
                     "for the last N specified number of dates")
class PersonsPerDate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('last_dates_count', type=int, help='The number of most recent dates to consider.')

    @api.doc(parser=parser, responses={200: "Success",
                                       400: "Bad Request",
                                       500: "Internal Server Error"})
    def get(self, last_dates_count):
        # TODO consider implementing timeout error handling
        # I understand I could specify the type of the parameter in the route
        # but in that case the API would return empty 404 error on wrong parameter type
        # Checking type here to return a correct error
        try:
            last_dates_count = int(last_dates_count)
        except ValueError:
            return 'Invalid parameter type, expected int', 400

        # Could also truncate results to 365 days
        # This wasn't in the requirements, but I couldn't think of any other
        # errors to implement
        if last_dates_count > 365:
            return 'Cannot return more than a year of records', 400

        try:
            return bq_api.get_persons_per_date(last_dates_count)
        except Exception as e:
            # log error
            return "Unknown Error Occurred", 500


@api.route('/procedure_usage/<procedure_type>', methods=['GET'])
@api.doc(description="This function retrieves the number of distinct persons "
                     "and providers per date for a specified procedure type "
                     "from the BigQuery dataset. It returns the results as a JSON string.")
class ProcedureUsage(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('procedure_type', type=int, help='The concept ID of the procedure type to consider.')

    @api.doc(parser=parser, responses={200: "Success",
                                       400: "Bad Request",
                                       500: "Internal Server Error"})
    def get(self, procedure_type):
        try:
            procedure_type = int(procedure_type)
        except ValueError:
            return 'Invalid parameter type, expected int', 400

        try:
            return bq_api.get_procedure_usage(procedure_type)
        except Exception as e:
            # log error
            return "Unknown Error Occurred", 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
