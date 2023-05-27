

# https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def test_group_bar_chart(chart_title='my chart title', col_groups=None, col_groups_data=None,
           x_label='x label', x_min=None, x_max=None,
           y_label='y label', y_min=None, y_max=None
):
    if col_groups is None:
        msg = "Column groups is None"
        raise SystemError(msg)
    if col_groups_data is None:
        msg = "Column Groups Data is None"
        raise SystemError(msg)

    fig, ax = plt.subplots(layout='constrained')

    x = np.arange(len(col_groups))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    for k, v in col_groups_data.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, v, width, label=k)
        ax.bar_label(rects, padding=3)

        # todo: START- add a % in the middle of the bars, need to generalise it
        texts_x = x + offset
        texts_x -= width/2.2
        texts_y = np.array(v) / 2

        text_lst = [10, 20, 30, 40, 10, 20, 30, 40]
        text_font = {
            'family': 'serif',
            'color': 'black',
            'weight': 'normal',
            'size': 8
        }

        for i in range(len(texts_x)):
            plt.text(x=texts_x[i], y=texts_y[i], s=f'{text_lst[i]}%')

        # todo: END - add a % in the middle of the bars, need to generalise it

        multiplier += 1

    # ax.plot(col_groups, col_groups_data['dev_no_jira'], color='black')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(chart_title)
    ax.set_xticks(x + width, col_groups)
    ax.legend(loc='upper left', ncols=len(col_groups_data.keys()))

    if y_min is not None and y_max is not None:
        ax.set_ylim(y_min, y_max)
    elif y_min is not None:
        ax.set_ylim(y_min)

    plt.show()


if __name__ == "__main__":
    # COL_GROUPS = ["2023-W1", "2023-W2", "2023-W3", "2023-W4"]
    data = {
        'year_month': ["2023-W1", "2023-W2", "2023-W3", "2023-W4"],
        'rainy_day': [80, 125, 200, 240],
        'sunny_day': [220, 175, 100, 60],
        'total_days': [300, 300, 300, 300]
    }

    # for k, v in data.items():
    #     print(k)
    #     print(v)
    #     print()
    #
    #     input('wait ah')

    df = pd.DataFrame(data)
    print(df, '\n')

    y_min = min(df[['total_days', 'rainy_day']].min())
    if y_min > 0:
        y_min = 0

    y_max = max(df[['total_days', 'rainy_day']].max()) * 1.2

    print(y_min, y_max)

    COL_GROUPS = df['year_month'].tolist()
    COL_GROUPS_DATA = df[['total_days', 'rainy_day']].to_dict(orient='list')

    print(COL_GROUPS)
    print()
    for k, v in COL_GROUPS_DATA.items():
        print(k, ': ', v)

    test_group_bar_chart(chart_title='title 3',
                         col_groups=COL_GROUPS, col_groups_data=COL_GROUPS_DATA,
                         y_min=y_min, y_max=y_max)
