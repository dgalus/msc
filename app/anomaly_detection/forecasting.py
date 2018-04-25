import collections

class Error(Exception):
    """
    Base class for custom exceptions.
    """
    pass

class BadArgumentTypeError(Error):
    """Exception raised for wrong type passed to function.
    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """
    def __init__(self, expression, message):
        super().__init__()
        self.expression = expression
        self.message = message

def initial_trend(series, season_length):
    """
    Calculates initial trend.
    Arguments:
    - series (list with float values)
    - season_length (int).
    Returns: initial trend value.
    """
    s = 0.0
    for i in range(season_length):
        s += float(series[i+season_length] - series[i]) / season_length
    return s/season_length

def initial_seasonal_components(series, season_length):
    """
    Calculates initial seasonal components.
    Arguments:
    - series (list with float values)
    - season_length (int).
    Returns: season-length array of seasonal components.
    """
    seasonals = {}
    season_averages = []
    n_seasons = int(len(series)/season_length)
    for j in range(n_seasons):
        season_averages.append(
            sum(series[season_length*j:season_length+season_length])/float(season_length)
        )
    for i in range(season_length):
        sum_of_vals_avg = 0.0
        for j in range(n_seasons):
            sum_of_vals_avg += series[season_length*j+i]-season_averages[j]
        seasonals[i] = sum_of_vals_avg/n_seasons
    return seasonals

def holt_winters_forecast(series, season_length, alpha, beta, gamma, n_preds):
    """
    Holt winters forecast (triple exponential smoothing forecast).
    Arguments:
    - series (list with float values)
    - season_length (int)
    - alpha (float; how fast previous samples will be forgotten)
    - beta (float; trend factor)
    - gamma (float; smoothing factor for the seasonal component)
    - n_preds (int; number of points into the future)
    Returns: list with forecast values.
    """
    try:
        result = []
        seasonals = initial_seasonal_components(series, season_length)
        for i in range(len(series) + n_preds):
            if i == 0:
                smooth = series[0]
                trend = initial_trend(series, season_length)
                result.append(series[0])
                continue
            if i >= len(series):
                m = i-len(series)+1
                result.append((smooth+m*trend) + seasonals[i%season_length])
            else:
                val = series[i]
                last_smooth = smooth
                smooth = alpha*(val-seasonals[i%season_length])+(1-alpha)*(smooth+trend)
                trend = beta*(smooth-last_smooth)+(1-beta)*trend
                seasonals[i%season_length] = gamma*(val-smooth)+(1-gamma)*seasonals[i%season_length]
                result.append(smooth+trend+seasonals[i%season_length])
        return result
    except Exception:
        raise BadArgumentTypeError(
            "forecasting.holt_winters.holt_winters_forecast()",
            "Some argument is wrong type."
        )