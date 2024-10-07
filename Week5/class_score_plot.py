import os
import matplotlib.pyplot as plt

def read_data(filename):
    data = []
    with open(os.path.join(os.path.dirname(__file__), filename), 'r') as f:
        for line in f.readlines():
            if not line.startswith('#'): # If 'line' is not a header
                data.append([int(word) for word in line.split(',')])
    return data

if __name__ == '__main__':
    # Load score data
    class_kr = read_data('data/class_score_kr.csv')
    class_en = read_data('data/class_score_en.csv')

    # Prepare midterm, final, and total scores
    midterm_kr, final_kr = zip(*class_kr)
    total_kr = [40/125*midterm + 60/100*final for (midterm, final) in class_kr]
    midterm_en, final_en = zip(*class_en)
    total_en = [40/125*midterm + 60/100*final for (midterm, final) in class_en]

    # Plot midterm/final scores as points
    plt.figure(1)
    plt.grid(True)
    plt.axis([0, 125, 0, 100])
    plt.xlabel('Midterm scores')
    plt.ylabel('Final scores')
    plt.scatter(midterm_kr, final_kr, color='red', marker='o', label='Korean')
    plt.scatter(midterm_en, final_en, color='blue', marker='+', label='English')
    plt.legend()
    
    # Plot total scores as a histogram
    plt.figure(2)
    plt.xlim([0, 100])
    plt.xlabel('Total scores')
    plt.ylabel('The number of students')
    plt.hist(total_kr, bins=20, range=(0, 100), alpha=0.3, color='red', label='Korean')
    plt.hist(total_en, bins=20, range=(0, 100), alpha=0.3, color='blue', label='English')
    plt.legend()

    plt.show()