import csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class FitnessIndicator: 
    def __init__(self, file_location):
        self.file_location = file_location
        self.data = []
        self.read_csv_data()

    def read_csv_data(self):
        with open(self.file_location, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.data.append(row)

    def calculate_normalize_score(self, score, min_score, max_score):
        score = float(score)
        normalized_score = int(max(((score - min_score) / (max_score - min_score)), 0) * 100)
        return normalized_score

    def calculate_average_scores(self, *args):
        if not args:
            return 0
        total = sum(args)
        average = round(total / len(args), 0)
        return average

    def process_data(self):
        results = []
        for row in self.data:
            push_up_norm = self.calculate_normalize_score(row['push_up'], 15, 99)
            pull_up_norm = self.calculate_normalize_score(row['pull_up'], 5, 37)
            squats_norm = self.calculate_normalize_score(row['squats'], 16, 178)
            fivekm_time_norm = self.calculate_normalize_score(row['fivekm_time'], 31.5, 19.75)
            crunches_norm = self.calculate_normalize_score(row['crunches'], 23, 159)
            bench_press_norm = self.calculate_normalize_score(row['bench_press'], 47, 98)
            squat_norm = self.calculate_normalize_score(row['squat'], 60, 130)
            overhead_press_norm = self.calculate_normalize_score(row['overhead_press'], 30, 87)

            overall_score = self.calculate_average_scores(
                push_up_norm, pull_up_norm, squats_norm, fivekm_time_norm,
                crunches_norm, bench_press_norm, squat_norm, overhead_press_norm
            )

            results.append({
                'date': row['date'],
                'overall_score': overall_score,
                'push_up_norm': push_up_norm,
                'pull_up_norm': pull_up_norm,
                'squats_norm': squats_norm,
                'fivekm_time_norm': fivekm_time_norm,
                'crunches_norm': crunches_norm,
                'bench_press_norm': bench_press_norm,
                'squat_norm': squat_norm,
                'overhead_press_norm': overhead_press_norm,
            })

        return results

    def save_results(self, results):
        csv_file_location = 'results/fitness_results.csv'
        with open(csv_file_location, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

    def plot_results(self):
        data = pd.read_csv('results/fitness_results.csv')
        data['date'] = pd.to_datetime(data['date'])
        data.set_index('date', inplace=True)

        plt.figure(figsize=(12, 8))
        palette = sns.color_palette("tab10", n_colors=8)

        sns.lineplot(data=data[['push_up_norm', 'pull_up_norm', 'squats_norm',
                                'fivekm_time_norm', 'crunches_norm', 
                                'bench_press_norm', 'squat_norm', 
                                'overhead_press_norm']], palette=palette)

        sns.lineplot(data=data['overall_score'], color='black', linewidth=3, label='Overall Score')

        plt.title('Normalized Fitness Scores Over Time')
        plt.xlabel('Date')
        plt.ylabel('Normalized Score')

        handles = [plt.Line2D([0], [0], color=palette[i], lw=2) for i in range(8)]
        handles.append(plt.Line2D([0], [0], color='black', lw=3))

        plt.legend(handles=handles, title='Exercises', 
                   labels=['Push Up level', 'Pull Up level', 'Squats level', '5KM Time level', 
                           'Crunches level', 'Bench Press level', 'Squat level', 'Overhead Press level',
                           'Overall level'], 
                   bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=4)

        plt.grid()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('results/fitness_scores_over_time.png', dpi=300)

    def run(self):
        results = self.process_data()
        self.save_results(results)
        self.plot_results()


file_location = 'inputs/input_pbs.csv'
fitness_indicator = FitnessIndicator(file_location)
fitness_indicator.run()
