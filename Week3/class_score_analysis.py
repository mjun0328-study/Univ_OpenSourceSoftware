import os

def read_data(filename):
    f = open(os.path.join(os.path.dirname(__file__), filename), 'r')
    data = []
    index = 0
    for line in f.read().split('\n'):
        if(index < 1):
            index += 1
            continue
        data.append(tuple(map(int, line.split(','))))
    return data

def calc_weighted_average(data_2d, weight):
    average = []
    for row in data_2d:
        average.append(row[0] * weight[0] + row[1] * weight[1])
    return average

def analyze_data(data_1d):
    length = len(data_1d)

    mean = 0
    for row in data_1d:
        mean += row
    mean /= length

    var = 0
    for row in data_1d:
        var += (row - mean) ** 2
    var /= length

    data_1d.sort()
    if length % 2 == 0:
        median = (data_1d[length//2-1] + data_1d[length//2]) / 2
    else:
        median = data_1d[length//2]

    return mean, var, median, min(data_1d), max(data_1d)

if __name__ == '__main__':
    data = read_data('data/class_score_en.csv')
    if data and len(data[0]) == 2: # Check 'data' is valid
        average = calc_weighted_average(data, [40/125, 60/100])

        # Write the analysis report as a markdown file
        with open(os.path.join(os.path.dirname(__file__), 'class_score_analysis.md'), 'w') as report:
            report.write('### Individual Score\n\n')
            report.write('| Midterm | Final | Average |\n')
            report.write('| ------- | ----- | ----- |\n')
            for ((m_score, f_score), a_score) in zip(data, average):
                report.write(f'| {m_score} | {f_score} | {a_score:.3f} |\n')
            report.write('\n\n\n')

            report.write('### Examination Analysis\n')
            data_columns = {
                'Midterm': [m_score for m_score, _ in data],
                'Final'  : [f_score for _, f_score in data],
                'Average': average }
            for name, column in data_columns.items():
                mean, var, median, min_, max_ = analyze_data(column)
                report.write(f'* {name}\n')
                report.write(f'  * Mean: **{mean:.3f}**\n')
                report.write(f'  * Variance: {var:.3f}\n')
                report.write(f'  * Median: **{median:.3f}**\n')
                report.write(f'  * Min/Max: ({min_:.3f}, {max_:.3f})\n')