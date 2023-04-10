import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from typing import Optional


class ParetoChart:
    def __init__(self, data: pd.DataFrame, cat_col: str, cat_col_title: str,
                 numeric_col: Optional[str] = None, numeric_col_title: Optional[str] = None,
                 chart_title: Optional[str] = None):
        self._df = data
        self._cat_col = cat_col
        self._cat_col_title = cat_col_title
        self._num_col = numeric_col
        self._num_col_title = numeric_col_title
        self._chart_title = chart_title

        self._t_table = None

    @property
    def t_table(self):
        return self._t_table

    def tally_table(self):
        if self._num_col is None:
            # default is to do 'freq count'
            self._num_col = 'freq'
            f = self._df[self._cat_col]
            f = f.value_counts()
            df = pd.DataFrame({self._cat_col: f.keys(), 'freq': f.values})
        else:
            f = self._df[[self._cat_col, self._num_col]].groupby(self._cat_col).sum().round(2)
            df = f.reset_index()

        df.sort_values(by=self._num_col, ascending=False, inplace=True)
        df['pct'] = (df[self._num_col] / df[self._num_col].sum() * 100).round(2)
        df['cumulative_pct'] = (df[self._num_col].cumsum() / df[self._num_col].sum() * 100).round(2)
        df = df.reset_index(drop=True)
        self._t_table = df
        return df

    def pareto_plot(self):
        # sns.set_theme(style="white", palette=None)
        sns.set_theme(style="white", palette="pastel")
        fig, ax = plt.subplots()

        chart_title = f"Pareto Chart - {self._num_col}" if self._chart_title is None else self._chart_title
        plt.title(label=chart_title, fontsize=20, color="green", pad='10.0')

        sns.barplot(ax=ax, x=self._cat_col, y=self._num_col, data=self._t_table)
        # ax.bar(x=self._cat_col, height=self._num_col, data=self._t_table)

        if self._cat_col_title is None:
            ax.set_xlabel(self._cat_col)
        else:
            ax.set_xlabel(self._cat_col_title)

        if self._num_col_title is None:
            ax.set_ylabel(self._num_col)
        else:
            ax.set_ylabel(self._num_col_title)
        ax.set_ylim(ymin=0)

        ax2 = ax.twinx()
        # ax2.plot(col_x, 'cumulative_pct', data=data, marker='o', color='red');
        sns.lineplot(ax=ax2, data=self._t_table, x=self._cat_col, y='cumulative_pct', color='red', marker='o')
        ax2.set_ylabel("cumulative %")
        ax2.set_ylim(ymin=0)
        ax2.axhline(80, color="orange", linestyle="dashed")
        ax2.yaxis.set_major_formatter(PercentFormatter())
        plt.show()

        print()
        print(self._t_table.set_index(self._cat_col).T)

    def create(self):
        self.tally_table()
        self.pareto_plot()


def test_plotting_fns():
    df = pd.read_excel("DA-LSS.xlsx", sheet_name='Reclaims', skiprows=6)

    pareto_by_incident_count = ParetoChart(
        data=df,
        cat_col="Person",
        cat_col_title='Staff'
    )
    pareto_by_incident_count.create()

    """
        def __init__(self, data: pd.DataFrame, cat_col: str, cat_col_title: str,
                 numeric_col: Optional[str], numeric_col_title: Optional[str],
                 chart_title: Optional[str]):

    """

    pareto_by_processing_time = ParetoChart(
        data=df,
        cat_col="Person",
        cat_col_title='Staff',
        numeric_col='Processing time',
        numeric_col_title='Processing time - minutes'
    )
    pareto_by_processing_time.create()

    print('\n')
    print("While Margrient and Marcel have the most incidents, ")
    print("Margrient's processing time is significantly longer than Marcel.")
    print('\n\n')


if __name__ == "__main__":
    test_plotting_fns()
