"""
[tech]
plotly for graphs
yfinance for stocks

[requirements]
graph with x=date, y=profit
one line for each security
line represents net profit at x
that's it, not too complicated tbh

[limitations]
dividend reinvesting? think about it
fractional trading? sure why not

[additional stuff]
some kind of tool to convert wealthsimple activity log into csv format

[flow]
we have a file
parse the file with FileParser -> Security[]
pass Security[] to HistoryProfitCalculator
define min_history_date and max_history_date based on min and max of Security[]
for each day between min and max:
    for each security:
        get close price for security on that date
        determine profit for that security at that date
        record this profit into a plot data structure
    
plot the data structure using Grapher

[limitations]
problem: stocks that don't exist in yfinance (or no longer exist even if they used to) break the program
fix: have some check at the start if a symbol exists. if not, remove it from the known securities

problem: weird data from yfinance
fix: idk, this usually happens with stocks that closed, ignore or remove manually

problem: no builtin functionality from wealthsimple to export trade history
fix: write a custom graphql API digest script
"""

from file_parse import parse_file
from history_profit_calculate import calculate_profit_history
from history_profit_graph import plot_graph

if __name__ == "__main__":
    security_symbol_to_history = parse_file("wealthsimple_trades.csv")
    history_profit = calculate_profit_history(security_symbol_to_history)

    plot_graph(history_profit)
