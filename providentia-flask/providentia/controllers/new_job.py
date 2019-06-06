import logging
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from config import default_config
from providentia.entities.benchmark import Benchmark

bp = Blueprint('new-job', __name__, )
config = default_config()
logging.basicConfig(level=config.LOGGING_LEVEL)


#######################################################################################################################
# REST Controllers
#######################################################################################################################


@bp.route("/", methods=['POST'])
@cross_origin()
def new_job():
    """Capture new job to begin processing."""
    import providentia.repository.benchmark_repository as bm_table

    data = request.get_json()
    logging.debug(data)

    # Check for uniqueness
    if bm_table.find_title(data['title']) is not None:
        logging.debug("Job title not unique!")
        return jsonify(error='Job title not unique!'), 400

    try:
        benchmark = deserialize(data)
    except KeyError as e:
        logging.debug(str(e))
        return jsonify(error=str(e)), 404

    bm_table.insert(benchmark)

    return jsonify(message='Not yet implemented.'), 200


#######################################################################################################################
# Object Functionality
#######################################################################################################################


def deserialize(obj):
    import providentia.repository.databases_repository as db_table
    import providentia.repository.datasets_repository as ds_table
    import providentia.repository.analysis_repository as an_table

    if type(obj) is dict:
        benchmark = Benchmark()

        database = db_table.find_name(obj['database'])
        dataset = ds_table.find_name(obj['dataset'])
        analysis = an_table.find_name(obj['analysis'])

        if database is None:
            raise KeyError('Database "{}" is not supported!'.format(obj['database']))
        if dataset is None:
            raise KeyError('Dataset "{}" is not supported!'.format(obj['dataset']))
        if analysis is None:
            raise KeyError('Analysis "{}" is not supported!'.format(obj['analysis']))

        benchmark.database = database.database_id
        benchmark.dataset = dataset.dataset_id
        benchmark.analysis = analysis.analysis_id
        benchmark.title = obj['title']
        benchmark.description = obj['description']
        benchmark.query_time = 0
        benchmark.analysis_time = 0

        return benchmark
    else:
        raise NotImplementedError("Cannot deserialize data that is not dict or JSON format.")