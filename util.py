command_dict = {"start": "Запуск бота",
                "help": "Cписок всех доступных команд",
                "train": "Генерирует подборку из задач"}


def output_available_commands(d: dict) -> str:
    l_tmp = []
    for key, value in d.items():
        s_tmp = f"/{key} – {value}"
        l_tmp.append(s_tmp)
    s = '\n'.join(l_tmp)
    return s


def strVec2str(s) -> str:
    '''
        input:
            R sample output: '[1] "document_id"'
        output:
            Python string: 'document_id'
    '''
    return str(s).split()[1][1:-1]
