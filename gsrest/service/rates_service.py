from cassandra.query import dict_factory
from cassandra.concurrent import execute_concurrent

from gsrest.db.cassandra import get_session
from gsrest.model.rates import ExchangeRate
from gsrest.service.general_service import get_statistics


RATES_TABLE = 'exchange_rates'


def get_rates(currency, height=-1):
    """ Returns the exchange rate for a given block height """

    if height == -1:
        height = get_statistics(currency)['no_blocks'] - 1

    session = get_session(currency, 'transformed')
    session.row_factory = dict_factory
    query = "SELECT * FROM exchange_rates WHERE height = %s"
    result = session.execute(query, [height])
    if result.current_rows:
        r = result.current_rows[0]
        return ExchangeRate(r['height'], {k: v for k, v in r.items()
                                          if k != 'height'}).to_dict()
    raise ValueError("Cannot find height {} in currency {}"
                     .format(height, currency))


def list_rates(currency, heights=-1):
    """ Returns the exchange rates for a list of block heights """
    session = get_session(currency, 'transformed')
    session.row_factory = dict_factory

    if heights == -1:
        heights = [get_statistics(currency)['no_blocks'] - 1]

    concurrent_query = "SELECT * FROM exchange_rates WHERE height = %s"
    statements_and_params = []
    for h in heights:
        statements_and_params.append((concurrent_query, [h]))
    rates = execute_concurrent(session, statements_and_params,
                               raise_on_first_error=False)
    height_rates = dict()  # key: height, value: {'eur': 0, 'usd':0}
    for (success, rate) in rates:
        if not success:
            pass
        else:
            d = rate.one()
            height_rates[d['height']] = {k: v for k, v in d.items()
                                         if k != 'height'}
    return height_rates
