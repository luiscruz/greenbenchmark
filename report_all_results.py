#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import pandas
import matplotlib.pyplot as plt
import numpy as np
import os
import statsmodels.api as sm
import scipy.stats
from tqdm import tqdm

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir) if os.path.isdir(os.path.join(a_dir, name))]

parser = argparse.ArgumentParser(description='Report a set of Odroid Energy Experiment Results.')
parser.add_argument('--all_figures', action='store_true')
parser.add_argument('--single_experiment', action='store_true')
parser.add_argument('results_directory', help='the directory with all the results')

args = parser.parse_args()

def read_energy_csv(results_directory):
    energy_csv = pandas.read_csv(results_directory+"/energy_log.csv", parse_dates=True)
    energy_csv['temperature'] = 0 #make it tolerant to data without temperature
    energy_csv =  pandas.DataFrame(
        [
            {
                'timestamp': k,
                'armW': v.armW.mean(),
                'memW': v.memW.mean(),
                'g3dW': v.g3dW.mean(),
                'kfcW': v.kfcW.mean(),
                'temperature': v.temperature.mean(),
            } for k,v in energy_csv.groupby(['timestamp'])
        ],
        columns=['timestamp', 'armW', 'memW', 'g3dW', 'kfcW', 'temperature']
    )
    energy_csv.index = energy_csv['timestamp']
    energy_csv['timestamp_delta'] = (energy_csv['timestamp']-energy_csv['timestamp'].shift()).fillna(0)
    return energy_csv

def read_event_csv(results_directory):
    event_csv = pandas.read_csv(results_directory+"/event_log.csv", index_col="event", parse_dates=['timestamp'])
    #interaction_start=event_csv['InteractionStarted', 'timestamp']
    #interaction_end=event_csv['InteractionEnded', 'timestamp']
    return event_csv

def calculate_energy(df_energy, t1,t2, power_feature):
    return df_energy.loc[t1:t2, [power_feature, 'timestamp_delta']].product(axis=1).sum()

def report_experiment(dir_path):
    df_energy = read_energy_csv(dir_path)
    power_features = ['armW','memW','g3dW','kfcW']
    df_event = read_event_csv(dir_path)
    interaction_start=df_event.loc['InteractionStarted', 'timestamp']
    interaction_end=df_event.loc['InteractionEnded', 'timestamp']

    dirname=os.path.basename(dir_path)
    experiment_name = dirname[:-17]
    experiment_timestamp=dirname[-16:]

    report_data = {'experiment':experiment_name,'timestamp':experiment_timestamp}
    report_data["temperature"] = df_energy["temperature"].mean()
    report_data["duration"] = int(interaction_end) - int(interaction_start)
    for power_feature in power_features:
        energy_consumption =  calculate_energy(df_energy,interaction_start,interaction_end, power_feature)
        if args.all_figures:
            plot_power_feature(df_energy, df_event, power_feature, "%s/%s.pdf"%(dir_path,power_feature), energy_consumption)
            plot_consumption(df_energy,power_feature,interaction_start,interaction_end,"%s/%s_consumption.png"%(dir_path,power_feature))
        report_data["energy_%s"%power_feature[:-1]]=energy_consumption
    return report_data

def cohensd(sample1, sample2):
    n1 = len(sample1.index)
    n2 = len(sample2.index)
    var1 = sample1.var()
    var2 = sample2.var()
    return (sample2.mean() - sample1.mean()) / np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))


def report_set_of_experiments(dir_path):
    experiments_report_data = []
    for subdir in tqdm(get_immediate_subdirectories(dir_path)):
        experiment_report_data = report_experiment(dir_path+"/"+subdir)
        experiments_report_data.append(experiment_report_data)
    df = pandas.DataFrame(experiments_report_data)
    df.to_csv(dir_path+"/_results.csv")

    df['energy_total'] = df[['energy_arm', 'energy_mem', 'energy_g3d', 'energy_kfc']].sum(axis=1)


    #Remove outliers 2 stds
    def replace(group, stds):
        group[np.abs(group - group.mean()) > stds * group.std()] = np.nan
        return group
    df.loc[:, df.columns == 'energy_arm'] = df.groupby('experiment').transform(lambda g: replace(g, stds=2))
    df.dropna(inplace=True)

    experiments = list(df['experiment'].unique())
    experiment_pivot = next(x for x in experiments if (x!='blank-app') and ('lint' not in x))
    df_experiment_pivot = df[df["experiment"] == experiment_pivot]
    df_grouped = df.groupby('experiment')
    experiments_without_blankapp = [experiment for experiment in experiments if experiment != 'blank-app']

    for energy_feature in ['energy_arm', 'energy_mem', 'energy_g3d', 'energy_kfc','energy_total']:

        report_energy_feature(df_grouped, df_experiment_pivot, energy_feature, dir_path)

        #violinplot
        plt.rcParams['figure.subplot.bottom'] = 0.23  # keep labels visible

        consumption_by_experiment = [df[energy_feature][df["experiment"] == experiment] for experiment in experiments_without_blankapp]

        def get_experiment_label(experiment, experiment_pivot):
            if experiment == experiment_pivot:
                return 'Original'
            else:
                experiment = experiment.replace(experiment_pivot+"-lint-", "")
                experiment = experiment.replace("-", " ").title()
            return experiment

        experiment_labels = [get_experiment_label(experiment, experiment_pivot) for experiment in experiments_without_blankapp]

        fig = plt.figure()
        ax = fig.add_subplot(111)
        sm.graphics.violinplot(consumption_by_experiment, ax=ax, labels=experiment_labels, plot_opts={'cutoff_val':5, 'cutoff_type':'abs','label_fontsize':'small', 'label_rotation':30})
        # ax.set_xlabel("App Version")
        ax.set_ylabel("Energy Consumption (J)")
        # plt.title("%s energy consumption by APK for %s"%(energy_feature[-3:].title(), experiment_pivot.replace('-',' ').title()))
        plt.savefig(dir_path+'/_violinplot_%s.pdf'%energy_feature, bbox_inches='tight')
        plt.close()






    # Scatter for Energy and Temperature
    plt.figure()
    df_without_blankapp = df[df["experiment"] != 'blank-app']
    df_without_blankapp["temperatureC"] = df_without_blankapp["temperature"]/1000
    plt.scatter(df_without_blankapp["temperatureC"] , df_without_blankapp['energy_arm'], s=30,
            c=df_without_blankapp['experiment'].apply(lambda x: experiments_without_blankapp.index(x)), cmap=plt.cm.get_cmap('jet', len(experiments_without_blankapp)), alpha=0.75)
    # fit with np.polyfit
    m, b = np.polyfit(df_without_blankapp["temperatureC"], df_without_blankapp['energy_arm'], 1)
    axes = plt.gca()
    X_plot = np.linspace(axes.get_xlim()[0],axes.get_xlim()[1],10)
    plt.plot(X_plot, m*X_plot + b, '-')

    plt.xlabel(u'Temperature (ºC)')
    plt.ylabel('Energy CPU (J)')
    # This function formatter will replace integers with target names
    formatter = plt.FuncFormatter(lambda val, loc: experiments_without_blankapp[val])
    # We must be sure to specify the ticks matching our target names
    plt.colorbar(ticks=range(len(experiments_without_blankapp)), format=formatter);

    plt.savefig(dir_path+'/_results_arm_scatter_energy_T.pdf')
    plt.close()
    #----------

    # Scatter for Energy and Duration
    plt.figure()
    plt.scatter(df_without_blankapp["duration"], df_without_blankapp['energy_arm'], s=30,
            c=df_without_blankapp['experiment'].apply(lambda x: experiments_without_blankapp.index(x)), cmap=plt.cm.get_cmap('jet', len(experiments_without_blankapp)), alpha=0.75)

    plt.ylabel('Energy CPU (J)')
    plt.xlabel('Duration (s)')
    # This function formatter will replace integers with target names
    formatter = plt.FuncFormatter(lambda val, loc: experiments_without_blankapp[val])
    # We must be sure to specify the ticks matching our target names
    plt.colorbar(ticks=range(len(experiments_without_blankapp)), format=formatter);

    plt.savefig(dir_path+'/_results_arm_scatter_energy_duration.pdf')
    plt.close()
    #----------

def report_energy_feature(df_grouped, df_experiment_pivot, energy_feature, dir_path):
    experiment_statistics = {}
    for experiment, group in df_grouped:
        row = {}
        row['sample_mean'] = group[energy_feature].mean()
        row['sample_std'] = group[energy_feature].std()
        row['n'] = len(group.index)
        row['shapiro_W'], row['shapiro_p'] = scipy.stats.shapiro(group[energy_feature], a=None, reta=False)
        row['mannwhitneyu_statistic'], pvalue = scipy.stats.mannwhitneyu(df_experiment_pivot[energy_feature], group[energy_feature], use_continuity=True)
        row['mannwhitneyu_p'] = pvalue*2 #this is a two-sided tail test
        row['welchsttest_statistic'], pvalue = scipy.stats.ttest_ind(df_experiment_pivot[energy_feature], group[energy_feature], equal_var=False)
        row['welchsttest_p'] = pvalue #this was already a two-tailed test
        row['mean_difference'] = group[energy_feature].mean() - df_experiment_pivot[energy_feature].mean()
        row['cohensd'] = cohensd(df_experiment_pivot[energy_feature],group[energy_feature])
        row['improvement'] = -row['mean_difference']/df_experiment_pivot[energy_feature].mean() # proportion of improvement
        row['savings_after24h'] =row['improvement']*24*60
        experiment_statistics[experiment] = row
    df_statistics = pandas.DataFrame.from_dict(experiment_statistics, orient='index')
    df_statistics.to_csv(dir_path+"/_%s_statistics.csv"%energy_feature)

    pandas.options.display.float_format = '{:,.2f}'.format
    with open(dir_path+"/_%s_descriptive_statistics.tex"%energy_feature, "w") as f:
        df_statistics[['n','sample_mean','sample_std']].to_latex(buf=f)
    with open(dir_path+"/_%s_significance_tests.tex"%energy_feature, "w") as f:
        df_statistics[['welchsttest_statistic','welchsttest_p']].to_latex(buf=f)
    with open(dir_path+"/_%s_effect_size.tex"%energy_feature, "w") as f:
        df_statistics[['mean_difference','cohensd','improvement','savings_after24h']].to_latex(buf=f)
    with open(dir_path+"/_%s_all_stats.tex"%energy_feature, "w") as f:
        df_statistics[['n','sample_mean','sample_std','mean_difference','welchsttest_statistic','welchsttest_p','cohensd','improvement','savings_after24h']].to_latex(buf=f)



def plot_power_feature(df_energy, df_event, power_feature, filename, energy_consumption=None, ymax=None):
    plt.figure()
    ax = df_energy[power_feature].plot(color='darkblue',linewidth=1.0)
    for (event,timestamp) in df_event.iterrows():
        timestamp = timestamp.values[0]
        ax.axvline(timestamp, color='darkblue', linestyle='--', alpha=0.5, linewidth=2)

    textY = (df_energy[power_feature].max() - df_energy[power_feature].min())*0.9
    arrowY = df_energy[power_feature].max()
    bbox_props = dict(boxstyle="round", fc="w", ec="none", alpha=0.9)
    arrowprops=dict(arrowstyle="->")
    ax.annotate('t0 - InteractionStarted', xy=(df_event.loc['InteractionStarted'], arrowY), xytext=(df_event.loc['InteractionStarted'], textY),ha="left",
            arrowprops=arrowprops,bbox=bbox_props
            )
    ax.annotate('tn - InteractionEnded', xy=(df_event.loc['InteractionEnded'], arrowY), xytext=(df_event.loc['InteractionEnded'], textY), ha="right",
            arrowprops=arrowprops,bbox=bbox_props
            )

    bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.7)
    textX = df_energy.index[len(df_energy.index)/2]
    textY = (df_energy[power_feature].max() - df_energy[power_feature].min())*0.1
    t = ax.text(textX, textY, "Area=%.2fJ"%energy_consumption, ha="center", va="center", size=15, bbox=bbox_props)
    ax.set_ylabel("Power (W)")
    ax.set_xlabel("Timestamp (s)")
    ax.get_xaxis().get_offset_text().set_visible(False) # remove exponential offset from axis

    if ymax:
        ax.set_ylim([0,ymax])
    if energy_consumption:
        plt.title("Energy consumption: %.2fJ"%(energy_consumption))
    else:
        plt.title("Plot of %s"%(power_feature))
    df_energy_to_fill = df_energy.loc[int(df_event.loc['InteractionStarted']):int(df_event.loc['InteractionEnded'])]
    ax.fill_between(df_energy_to_fill.index, 0, df_energy_to_fill[power_feature], edgecolor='none', facecolor='lightgray')

    plt.savefig(filename)
    plt.close()

def plot_consumption(df_energy,power_feature, start, end, filename):
    consumption_feature = power_feature+"acum_energy"
    df = df_energy.loc[start:end, ["timestamp_delta",power_feature]]
    df.loc[:, consumption_feature] = np.zeros(len(df.index))
    for i in range(1,len(df.index)):
        consumption = df.iloc[i-1][consumption_feature] + df.iloc[i][power_feature]*df.iloc[i]["timestamp_delta"]
        df.iloc[i][consumption_feature] = consumption
    plt.figure()
    ax = df[consumption_feature].plot()
    plt.title("Plot of %s"%(power_feature))
    plt.title("Plot of %s\nEnergy consumption: %.2fJ"%(power_feature,df.iloc[-1][consumption_feature]))
    plt.savefig(filename)
    plt.close()


if args.single_experiment:
    report_experiment(args.results_directory)
else:
    report_set_of_experiments(args.results_directory)
