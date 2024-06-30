from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd

def load_excel_data(character, move_type):
    file_path = f'data/{character}.xlsx'
    sheet_name = move_type
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    df.columns = df.columns.str.replace(' ', '').str.replace('(', '').str.replace(')', '')  # 列名を整形
    return df

def index(request):
    characters = ['Ryu', 'Ken']  # キャラクターのリスト
    move_types = ['通常技', '特殊技', '必殺技', 'SA']  # 技タイプのリストに 'SA' を追加

    selected_character = None
    selected_move_type = None
    selected_move_name = None
    selected_strength = None
    selected_derivative = None
    move_data = []
    has_strength = False
    has_derivative = False
    move_names = []
    strengths = []
    derivatives = []

    if request.method == 'POST':
        selected_character = request.POST.get('character')
        selected_move_type = request.POST.get('move_type')
        selected_move_name = request.POST.get('move_name')
        selected_strength = request.POST.get('strength')
        selected_derivative = request.POST.get('derivative')

        df = load_excel_data(selected_character, selected_move_type)

        move_names = df['技'].unique().tolist()
        
        if selected_move_name:
            filtered_df = df[df['技'] == selected_move_name]
            has_strength = not filtered_df['強度'].dropna().empty
            has_derivative = not filtered_df['派生'].dropna().empty

            if has_strength:
                strengths = filtered_df['強度'].dropna().unique().tolist()
            if has_derivative:
                derivatives = filtered_df['派生'].dropna().unique().tolist()

        if selected_strength:
            df = df[df['強度'] == selected_strength]
        if selected_derivative:
            df = df[df['派生'] == selected_derivative]

        # NaNを空文字列に変換
        df = df.fillna('')

        move_data = df[df['技'] == selected_move_name].to_dict(orient='records')

    return render(request, 'moves/index.html', {
        'characters': characters,
        'move_types': move_types,
        'move_names': move_names,
        'strengths': strengths,
        'derivatives': derivatives,
        'move_data': move_data,
        'selected_character': selected_character,
        'selected_move_type': selected_move_type,
        'selected_move_name': selected_move_name,
        'selected_strength': selected_strength,
        'selected_derivative': selected_derivative,
        'has_strength': has_strength,
        'has_derivative': has_derivative,
    })

def get_move_names(request):
    character = request.GET.get('character')
    move_type = request.GET.get('move_type')
    df = load_excel_data(character, move_type)
    move_names = df['技'].unique().tolist()
    return JsonResponse({'move_names': move_names})

def get_strengths_and_derivatives(request):
    character = request.GET.get('character')
    move_type = request.GET.get('move_type')
    move_name = request.GET.get('move_name')
    df = load_excel_data(character, move_type)
    df_filtered = df[df['技'] == move_name]
    strengths = df_filtered['強度'].dropna().unique().tolist()
    derivatives = df_filtered['派生'].dropna().unique().tolist()
    return JsonResponse({'strengths': strengths, 'derivatives': derivatives})
