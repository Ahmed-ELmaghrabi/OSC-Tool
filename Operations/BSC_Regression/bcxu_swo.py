import pandas as pd
import numpy as np
import json
# from ...Test05_App import app
from Base_Module import start, SHELL, send_ftp, get_ftp, client
import time
import datetime
import pathlib2
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from .Case_Result import usecase_output
# get relative data folder
# PATH = pathlib2.Path(__file__).parent

def bcxuswo(var):
    if var != 0:
        while(var):
            global options
            options = []
            VM_path = '/opt/jetty/Mbackup/kkx/BCXU/'
            local_path = 'C:\\Users\\aelmaghrabi\PycharmProjects\Prototype\Test05\\'
            BSC_Regression = 'C:\\Users\\aelmaghrabi\PycharmProjects\Prototype\Test05\Operations\BSC_Regression\\'
            Log_path = 'C:\\Users\\aelmaghrabi\PycharmProjects\Prototype\Test05\Log_History\\'
            send_ftp(local_path, VM_path, 'username.txt')
            send_ftp(local_path, VM_path, 'password.txt')
            send_ftp(local_path, VM_path, 'ipaddress.txt')
            time.sleep(1)
            # prepare = SHELL('sudo rm /opt/jetty/Mbackup/kkx/BCXU/btsid.txt')
            ex = SHELL('sudo /opt/jetty/Mbackup/kkx/BCXU/begin.sh')
            if ex == 0:
                bts_check = SHELL('cat /opt/jetty/Mbackup/kkx/BCXU/begin.csv')
                if bts_check == 0:
                    global new_df
                    get_ftp(VM_path+'begin.csv',BSC_Regression+'begin.csv')
                    df = pd.read_csv(BSC_Regression+'begin.csv')
                    new_df = df[
                        df['spawn ssh SYSTEM@10.199.139.4'].str.contains('BTS-', regex=True, case=True, na=False)]
                    new_df = new_df[~new_df['spawn ssh SYSTEM@10.199.139.4'].str.contains('SBTS')]

                    # new_df['spawn ssh SYSTEM@10.199.139.4'].str.split(' ',expand=True,n=4)
                    new_df[['spawn ssh SYSTEM@10.199.139.4', '2', '3', 'BTS', '5', '6']] = new_df[
                        'spawn ssh SYSTEM@10.199.139.4'].str.split(' ', expand=True, n=5)
                    new_df[['BTS', 'BTS_ID']] = new_df['BTS'].str.split('-', expand=True, n=1)

                text = 'Operation Executed Successfully'
                color = 'limegreen'
                Feedback = html.P('now, please enter your target BTS '
                                  'Then activate and wait for the execution',
                                  style={
                                      'font-weight':'bold',
                                      'font-color':'navy'
                                  }
                                  )
                var -= 1
                return Feedback, [{'label': i, 'value': i} for i in new_df['BTS_ID']]

def extended_bcxuswo(BTS,var):
    while(var):
        global options
        options = []
        ex = SHELL('sudo /opt/jetty/Mbackup/kkx/BCXU/bcxuswo.sh')
        if ex == 0:
            var -= 1
            time.sleep(1)
            text = 'Operation Executed Successfully'
            color = 'limegreen'
            Feedback = html.Div(
                    dbc.Fade(
                        dbc.Card(usecase_output(f'{text}', f'{color}'),
                             color='dark',
                             outline=True,
                             style={
                                 'width': '27.7rem',
                                 'margin-top': '2px',
                                 'margin-bottom': '4px'
                             }),
                        id='fade',
                        is_in=True,
                        appear=False),
                    # persistence=True, persistence_type="local",
                )
            return Feedback