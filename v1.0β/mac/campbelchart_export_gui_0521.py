# ライブラリの読み込み
import matplotlib.pyplot as plt
import matplotlib as mpl
import japanize_matplotlib
import pandas as pd
import glob
import os
import numpy as np
import PySimpleGUI as sg
import configparser
import shutil
import io

plt.rcParams['font.family'] = "02UtsukushiMincho"


# 初期化ファイルの読み込み
def import_ini(filepath_ini):
    config = configparser.ConfigParser()
    config.read(filepath_ini)
    return config


#キャンベル線図を１つ描画・保存する処理

def export_fig(filepath_input, config):
    subtitle = export_subtitle(filepath_input)
    
    df_limit = preprocessing_df(filepath_input, config)
    fig = draw_graph(df_limit, subtitle, config)
    
    return fig

def export_subtitle(filepath_input):
    testname = os.path.dirname(filepath_input).split("/")[-1]
    sensor = os.path.basename(filepath_input).split(".")[0]
    subtitle = sensor + "/" + testname
    return subtitle

def preprocessing_df(filepath_input, config):
    df = pd.read_csv(filepath_input, header=3)
    
    #グラフの描画を早めるための処理。不要な周波数帯域をカットする。
    df_temp = df[df["Hz/rpm"]<=int(config["axis"]["y_range_max"])]
    df_limit = df_temp[df_temp["Hz/rpm"]>=int(config["axis"]["y_range_min"])]
    df_limit.reset_index(inplace=True, drop=True)
    return df_limit


def draw_graph(df_limit, subtitle, config):
    # 空のグラフの生成
    fig = plt.figure(dpi=150)
    ax = fig.add_subplot(111)
    
    # タイトル・軸ラベルの設定
    ax.set_title(config["graph"]["title"], loc='left')
    ax.set_xlabel(config["axis"]["xlabel"])
    ax.set_ylabel(config["axis"]["ylabel"])
    ax.text(0.99, 1.05, subtitle, size=8, va='top', ha='right', transform=ax.transAxes)
    
    # キャンベル線図と補助線の描画
    if(config["supplementaryline"]["draw"]=="True"):
        draw_graphs_nthdegree(ax, config)
    mappable = draw_campbellchart(df_limit, ax, config)
    
    # 変域、カラーバーの設定
    if config["axis"]["x_auto"]=="False":
        plt.xlim([int(config["axis"]["x_range_min"]),int(config["axis"]["x_range_max"])])
    if config["axis"]["y_auto"]=="False":
        plt.ylim([int(config["axis"]["y_range_min"]),int(config["axis"]["y_range_max"])])
    plt.colorbar(mappable, ax=ax, label=config["axis"]["zlabel"])
    #plt.grid(alpha=0.1)
    plt.legend(bbox_to_anchor=(0, 1), loc='upper left', borderaxespad=0.2, fancybox=True, framealpha=1)
    
    return fig


def draw_graphs_nthdegree(ax, config):
    rpm = np.arange(0, 3001, 1000)
    #rpm = np.arange(x_range_min, x_range_max, 50)
    
    hz = rpm/60
    ub_freq = hz
    nz_freq = hz*int(config["supplementaryline"]["blades_number"])
    cg_freq = hz*int(config["supplementaryline"]["cogging_number"])
    
    ub_color="m"
    nz_color="y"
    cg_color="k"
    ub_linestyle = "-"
    nz_linestyle = "-"
    cg_linestyle = "-"
    ub_linewidth = 1
    nz_linewidth = 3
    cg_linewidth = 1
    ub_alpha=0.1
    nz_alpha=0.1
    cg_alpha=0.1
    
    ax.plot(rpm, ub_freq*1, color=ub_color, linestyle=ub_linestyle, linewidth=ub_linewidth, alpha=ub_alpha, label="UB")
    ax.plot(rpm, ub_freq*2, color=ub_color, linestyle=ub_linestyle, linewidth=ub_linewidth, alpha=ub_alpha)
    ax.plot(rpm, ub_freq*3, color=ub_color, linestyle=ub_linestyle, linewidth=ub_linewidth, alpha=ub_alpha)
    ax.plot(rpm, ub_freq*4, color=ub_color, linestyle=ub_linestyle, linewidth=ub_linewidth, alpha=ub_alpha)
    ax.plot(rpm, ub_freq*5, color=ub_color, linestyle=ub_linestyle, linewidth=ub_linewidth, alpha=ub_alpha)
    ax.plot(rpm, ub_freq*6, color=ub_color, linestyle=ub_linestyle, linewidth=ub_linewidth, alpha=ub_alpha)
    ax.plot(rpm, ub_freq*7, color=ub_color, linestyle=ub_linestyle, linewidth=ub_linewidth, alpha=ub_alpha)
    ax.plot(rpm, ub_freq*8, color=ub_color, linestyle=ub_linestyle, linewidth=ub_linewidth, alpha=ub_alpha)
    ax.plot(rpm, ub_freq*9, color=ub_color, linestyle=ub_linestyle, linewidth=ub_linewidth, alpha=ub_alpha)
    ax.plot(rpm, ub_freq*10, color=ub_color, linestyle=ub_linestyle, linewidth=ub_linewidth, alpha=ub_alpha)
    ax.plot(rpm, nz_freq*1, color=nz_color, linestyle=nz_linestyle, linewidth=nz_linewidth, alpha=nz_alpha, label="NZ")
    ax.plot(rpm, nz_freq*2, color=nz_color, linestyle=nz_linestyle, linewidth=nz_linewidth, alpha=nz_alpha)
    ax.plot(rpm, nz_freq*3, color=nz_color, linestyle=nz_linestyle, linewidth=nz_linewidth, alpha=nz_alpha)
    ax.plot(rpm, nz_freq*4, color=nz_color, linestyle=nz_linestyle, linewidth=nz_linewidth, alpha=nz_alpha)
    ax.plot(rpm, nz_freq*5, color=nz_color, linestyle=nz_linestyle, linewidth=nz_linewidth, alpha=nz_alpha)
    ax.plot(rpm, nz_freq*6, color=nz_color, linestyle=nz_linestyle, linewidth=nz_linewidth, alpha=nz_alpha)
    ax.plot(rpm, nz_freq*7, color=nz_color, linestyle=nz_linestyle, linewidth=nz_linewidth, alpha=nz_alpha)
    ax.plot(rpm, nz_freq*8, color=nz_color, linestyle=nz_linestyle, linewidth=nz_linewidth, alpha=nz_alpha)
    ax.plot(rpm, nz_freq*9, color=nz_color, linestyle=nz_linestyle, linewidth=nz_linewidth, alpha=nz_alpha)
    ax.plot(rpm, nz_freq*10, color=nz_color, linestyle=nz_linestyle, linewidth=nz_linewidth, alpha=nz_alpha)
    ax.plot(rpm, cg_freq*1, color=cg_color, linestyle=cg_linestyle, linewidth=cg_linewidth, alpha=cg_alpha, label="CG")
    ax.plot(rpm, cg_freq*2, color=cg_color, linestyle=cg_linestyle, linewidth=cg_linewidth, alpha=cg_alpha)
    ax.plot(rpm, cg_freq*3, color=cg_color, linestyle=cg_linestyle, linewidth=cg_linewidth, alpha=cg_alpha)
    ax.plot(rpm, cg_freq*4, color=cg_color, linestyle=cg_linestyle, linewidth=cg_linewidth, alpha=cg_alpha)
    ax.plot(rpm, cg_freq*5, color=cg_color, linestyle=cg_linestyle, linewidth=cg_linewidth, alpha=cg_alpha)
    ax.plot(rpm, cg_freq*6, color=cg_color, linestyle=cg_linestyle, linewidth=cg_linewidth, alpha=cg_alpha)
    ax.plot(rpm, cg_freq*7, color=cg_color, linestyle=cg_linestyle, linewidth=cg_linewidth, alpha=cg_alpha)
    ax.plot(rpm, cg_freq*8, color=cg_color, linestyle=cg_linestyle, linewidth=cg_linewidth, alpha=cg_alpha)
    ax.plot(rpm, cg_freq*9, color=cg_color, linestyle=cg_linestyle, linewidth=cg_linewidth, alpha=cg_alpha)
    ax.plot(rpm, cg_freq*10, color=cg_color, linestyle=cg_linestyle, linewidth=cg_linewidth, alpha=cg_alpha)


def draw_campbellchart(df_limit, ax, config):
    # 空のdf_plotを用意
    df_plot = pd.DataFrame(columns=["rpm", "Hz", "power"])
    
    # GraphR用のフォーマットから描画しやすいように"rpm,Hz,power"の3列に変換してdf_plotに格納
    for i in df_limit.columns:
        if(i != df_limit.columns[0]):
            x = np.full(len(df_limit),int(float(i)))
            df_x = pd.Series(x, name="rpm")
            df_y = df_limit["Hz/rpm"].rename("Hz")
            df_z = df_limit[i].rename("power")
            df_i = pd.concat([df_x, df_y, df_z], axis=1)
            df_plot = pd.concat([df_plot, df_i])
    
    # 描画するときに"power"の大きなものを上に描画するように、"power"の昇順で並び替える
    df_plot = df_plot.sort_values("power")
    
    # x,y,zにそれぞれのデータを格納する
    x = df_plot["rpm"]
    y = df_plot["Hz"]
    z = df_plot["power"]
    
    # z変域の定義
    #if config["axis"]["z_auto"]=="False":
    z_range_min = float(config["axis"]["z_range_min"])
    z_range_max = float(config["axis"]["z_range_max"])
    
    #描画(各軸のオートレンジの設定で場合分けがたくさんに。。。）
    size=30 #size=z*10  #size=(z-z.min())*80/(z.max()-z.min())
    if(config["axis"]["z_islog"]=="True"):
        if(config["axis"]["z_auto"]=="False"):
            mappable = ax.scatter(x, y, c=z, cmap='rainbow', s=size, marker=".", alpha=1, norm=mpl.colors.LogNorm(vmin=z_range_min, vmax=z_range_max))
        elif(config["axis"]["z_auto"]=="True"):
            mappable = ax.scatter(x, y, c=z, cmap='rainbow', s=size, marker=".", alpha=1, norm=mpl.colors.LogNorm())
    else:
        if(config["axis"]["z_auto"]=="False"):
            mappable = ax.scatter(x, y, c=z, cmap='rainbow', s=size, marker=".", alpha=1, vmin=z_range_min, vmax=z_range_max)
        elif(config["axis"]["z_auto"]=="True"):
            mappable = ax.scatter(x, y, c=z, cmap='rainbow', s=size, marker=".", alpha=1)
    return mappable


def proceccing_fig(fig, mode, window, filepath_output=""):
    #出力モードの設定（save:画像保存、show:画像表示、draw:GUIアプリ用）
    if mode=="save":
        fig.savefig(filepath_output)
        plt.clf()
        plt.close()
    
    elif mode=="show":
        plt.show()
    
    elif mode=="draw":
        fig_bytes = draw_plot_image(fig)
        window['-image-'].update(data=fig_bytes)

def export_filepath_output(filepath_input, folderpath_output):
    sensor = os.path.basename(filepath_input).split(".")[0]
    #.split(")")[0] + ")"
    filepath_output = os.path.join(folderpath_output, sensor + ".png")
    return filepath_output

def draw_plot_image(fig):
    item = io.BytesIO()
    plt.savefig(item, format='png')
    plt.clf()
    return item.getvalue()


#フォルダ内のすべてのデータからキャンベル線図を作る処理

def export_campbellcharts(folderpath_input, folderpath_output, config, window):
    # フォルダー構成をコピーする
    shutil.copytree(folderpath_input,folderpath_output, ignore=shutil.ignore_patterns('*.*'), dirs_exist_ok=True)

    # 処理するファイル一覧を取得する
    pathlist_input = glob.glob(os.path.join(folderpath_input, "**", "**.csv"), recursive=True)[0:]

    conti = True
    for i,filepath_input in enumerate(pathlist_input):
        fig = export_fig(filepath_input, config)
        filepath_output = return_filepath_output(folderpath_input, folderpath_output, filepath_input)
        print(filepath_input)
        print(filepath_output)
        proceccing_fig(fig, "save", window, filepath_output)

        if conti ==False:
            break
        conti =  sg.OneLineProgressMeter('グラフ出力の進捗', i + 1, len(pathlist_input), 'グラフ出力中・・・', keep_on_top=True)





#処理したファイルの格納先を返す処理
def return_filepath_output(folderpath_input, folderpath_output, filepath_input):
    file_name = filepath_input.replace(folderpath_input,"")[1:].replace(".csv", ".png")
    filepath_output = os.path.join(folderpath_output, file_name)
    return filepath_output



#GUIと処理




#GUI画面で設定された数値をconfigに保存する関数
def store_config(values):
    # temprate.iniを読み込む
    config = configparser.ConfigParser()
    #config.read(os.path.join(os.getcwd(),"ini", "template.ini"))
    
    # GUIに格納されている値をconfigに格納する
    config["graph"] = {"title" : str(values["title"])}
    config["axis"] = {
        "xlabel" : str(values["xlabel"]),
        "x_range_min" : str(values["x_range_min"]),
        "x_range_max" : str(values["x_range_max"]),
        "x_auto" : str(values["x_auto"]),
        "ylabel" : str(values["ylabel"]),
        "y_range_min" : str(values["y_range_min"]),
        "y_range_max" : str(values["y_range_max"]),
        "y_auto" : str(values["y_auto"]),
        "zlabel" : str(values["zlabel"]),
        "z_range_min" : str(values["z_range_min"]),
        "z_range_max" : str(values["z_range_max"]),
        "z_auto" : str(values["z_auto"]),
        "z_islog" : str(values["z_islog"]),}
    config["supplementaryline"] = {
        "draw" : str(values["draw"]),
        "blades_number" : str(values["blades_number"]),
        "cogging_number" : str(values["cogging_number"])}
    return config

def main():

    # テーマの設定
    sg.theme('DarkPurple6')
    use_custom_titlebar = False

    # フォントの定義
    font_0 = "_ 25"
    font_1 = "_ 20"
    font_2 = "_ 15"
    font_3 = "_ 10"

    # 画面左側の設定
    frame1_content = [
        [sg.Radio("入力ファイル選択（選択したファイルをグラフ化）", group_id=1, k="-RADIO_1-")],
        [sg.InputText(size=(50,1), k='-FILE_IN-'),sg.FileBrowse(button_text='参照', initial_folder=os.path.expanduser("~"))],
        [sg.Radio("入力フォルダ選択（選択したフォルダ中のファイルをすべてグラフ化）", group_id=1, k="-RADIO_2-")],
        [sg.InputText(size=(50,1), k='-FOLDER_IN-'),sg.FolderBrowse(button_text='参照', initial_folder=os.path.expanduser("~"))],
        [sg.Text("出力フォルダ選択")],
        [sg.InputText(size=(50,1), k='-FOLDER_OUT-'),sg.FolderBrowse(button_text='参照', initial_folder=os.path.expanduser("~"))],
        ]
        # [sg.Text("設定ファイル選択")],
        # [sg.InputText(size=(50,1), k='-INI-'),sg.FileBrowse(button_text='参照', initial_folder="./ini")]]

    frame2_content = [
        [sg.Text("読み込んだ設定ファイル："), sg.Text("", k="ini_name")],
        [sg.Text("グラフタイトル"), sg.InputText(key="title")],
        [sg.Text("")],
        [sg.Text("横軸のラベル　　　"), sg.InputText(key="xlabel")],
        [sg.Text("横軸の最大値　　　"), sg.InputText(key="x_range_max")],
        [sg.Text("横軸の最小値　　　"), sg.InputText(key="x_range_min")],
        [sg.Text("横軸オートスケール"), sg.Checkbox("",key="x_auto")],
        [sg.Text("縦軸のラベル　　　"), sg.InputText(key="ylabel")],
        [sg.Text("縦軸の最大値　　　"), sg.InputText(key="y_range_max")],
        [sg.Text("縦軸の最小値　　　"), sg.InputText(key="y_range_min")],
        [sg.Text("縦軸オートスケール"), sg.Checkbox("",key="y_auto")],
        [sg.Text("カラーバーのラベル"), sg.InputText(key="zlabel")],
        [sg.Text("カラーバーの最大値"), sg.InputText(key="z_range_max")],
        [sg.Text("カラーバーの最小値"), sg.InputText(key="z_range_min")],
        [sg.Text("カラーバーオートスケール"), sg.Checkbox("",key="z_auto")],
        [sg.Text("カラーバーをLOGスケールにする"), sg.Checkbox("", key="z_islog")],
        [sg.Text("")],
        [sg.Text("補助曲線を描画する"), sg.Checkbox("", key="draw")],
        [sg.Text("NZの次数（羽枚数）"), sg.InputText(key="blades_number")],
        [sg.Text("コギングの次数        "), sg.InputText(key="cogging_number")]]

    layout_left = [[sg.Frame('入出力選択', frame1_content, font=font_1, s=(360,190))],
        [sg.Button("グラフの表示(更新)", border_width=3, size=(15,1.1), k="-DRAW-"), sg.Button("グラフの処理・保存", border_width=3, size=(15,1.1), k="-SAVE-")],
        [sg.Frame("描画設定", frame2_content, font=font_1, s=(360,470))],
        [sg.Button("描画設定の読み込み", border_width=3, size=(15,1.1), k="-OPEN_INI-"), sg.Button("描画設定の保存", border_width=3, size=(15,1.1), k="-SAVE_INI-"), sg.Button("DEBUG", k="-DEBUG-")]]


    # 画面右側の設定
    frame2_content = [
        [sg.Image(filename='', key='-image-', background_color="white")]]

    layout_right = [[sg.Frame("キャンベル線図描画結果", frame2_content, font=font_1, s=(1000,770))]]

    # 画面全体の設定
    layout = [[[sg.T("キャンベル線図の描画ソフト", font=font_0, justification='c', expand_x=True)],
        [sg.Text(""), sg.Text("2022-5-21  v1.0β", font=font_2)],
        [sg.Col(layout_left), sg.Col(layout_right)]]]


    #windowの設定
    window = sg.Window('キャンベル線図の描画ソフト_v1.0β', layout, size=(1500, 1000), resizable=True, finalize=True)
    window.Maximize()


    #以下イベント処理
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: 
            break
        

        #「グラフの表示（更新）」ボタンを押した時の処理
        elif event == "-DRAW-":
            config = store_config(values)
            
            if(values["-RADIO_1-"]==1 and values["-FILE_IN-"]!=""):
                filepath_input = values["-FILE_IN-"]
                try:
                    fig = export_fig(filepath_input, config)
                    proceccing_fig(fig, "draw", window)
                except:
                    sg.popup("ファイルパスまたは設定にミスがあります", title="warning")
                    continue
            elif(values["-RADIO_2-"]==1):
                sg.popup("グラフを描画するには、「入力ファイルを選択」で１つファイルを指定してください。", title="warning")
            else:
                sg.popup("入力ファイルを選択してください", title="warning")
                continue
        

        #「グラフの処理・保存」ボタンを押した時の処理
        elif event == "-SAVE-":
            config = store_config(values)

            if values["-FOLDER_OUT-"]=="":
                sg.popup("出力フォルダを指定してください。", title="warning")
                continue
            elif(values["-RADIO_1-"]==1 and values["-FILE_IN-"]!=""):
                filepath_input = values["-FILE_IN-"]
                folderpath_output = values["-FOLDER_OUT-"]
                try:
                    fig = export_fig(filepath_input, config)
                    filepath_output = export_filepath_output(filepath_input, folderpath_output)
                    proceccing_fig(fig, "save", window, filepath_output)
                except:
                    sg.popup("ファイルパスまたは設定にミスがあります", title="warning2")
                    continue
            elif(values["-RADIO_2-"]==1):
                folderpath_input = values["-FOLDER_IN-"]
                folderpath_output = values["-FOLDER_OUT-"]
                try:
                    export_campbellcharts(folderpath_input, folderpath_output, config, window)
                except:
                    sg.popup("ファイルパスまたは設定にミスがあります", title="warning3")
                    continue
            else:
                sg.popup("入力ファイルを選択してください", title="warning")
                continue

        # elif event == "OK for 1 meter":
        #     print("test")
        #     #sg.one_line_progress_meter_cancel(key="-PROGRESS-")
        #     break


        #「描画設定の読み込み」ボタンを押した時の処理
        elif event == "-OPEN_INI-":
            filepath_ini_open = sg.popup_get_file("読み込む設定ファイルを選択してください",default_path=os.path.join(os.getcwd(),"ini"), no_window=True)
            #iniファイルが選択されなかった場合にループを抜ける処理
            if filepath_ini_open == "":
                continue
            
            try:
                config = configparser.ConfigParser()
                config.read(filepath_ini_open)
                #conofigの内容を読み出して、GUIの変数に格納していく
                window["title"].update(config["graph"]["title"])
                window["xlabel"].update(config["axis"]["xlabel"])
                window["x_range_min"].update(config["axis"]["x_range_min"])
                window["x_range_max"].update(config["axis"]["x_range_max"])
                if config["axis"]["x_auto"]=="True":
                    window["x_auto"].update(True)
                elif config["axis"]["x_auto"]=="False":
                    window["x_auto"].update(False)
                
                window["ylabel"].update(config["axis"]["ylabel"])
                window["y_range_min"].update(config["axis"]["y_range_min"])
                window["y_range_max"].update(config["axis"]["y_range_max"])
                if config["axis"]["y_auto"]=="True":
                    window["y_auto"].update(True)
                elif config["axis"]["y_auto"]=="False":
                    window["y_auto"].update(False)
                
                window["zlabel"].update(config["axis"]["zlabel"])
                window["z_range_min"].update(config["axis"]["z_range_min"])
                window["z_range_max"].update(config["axis"]["z_range_max"])
                if config["axis"]["z_auto"]=="True":
                    window["z_auto"].update(True)
                elif config["axis"]["z_auto"]=="False":
                    window["z_auto"].update(False)
                if config["axis"]["z_islog"]=="True":
                    window["z_islog"].update(True)
                elif config["axis"]["z_islog"]=="False":
                    window["z_islog"].update(False)
                
                if config["supplementaryline"]["draw"]=="True":
                    window["draw"].update(True)
                if config["supplementaryline"]["draw"]=="False":
                    window["draw"].update(False)
                window["blades_number"].update(config["supplementaryline"]["blades_number"])
                window["cogging_number"].update(config["supplementaryline"]["cogging_number"])
                window["ini_name"].update(os.path.basename(filepath_ini_open))
            except:
                sg.popup("設定ファイルが壊れています。")
                continue
        
        
        #「描画設定を保存」ボタンを押した時の処理
        elif event == "-SAVE_INI-":
            filepath_ini_save = sg.popup_get_file('saveas', save_as=True, default_path=os.path.expanduser("~"), no_window=True)
            
            #iniファイルが選択されなかった場合にループを抜ける処理
            if filepath_ini_save == "":
                continue
            config = store_config(values)
            with open(filepath_ini_save, 'w') as configfile:
                config.write(configfile)

        
        elif event == "-DEBUG-":
            # window["draw"].update(True)
            #sg.popup(values["-FOLDER_OUT-"])
            sg.popup(os. getcwd())

if __name__ == '__main__':
    main()