def buscar_tema_por_id(id_tema, temas):
    """
    Busca un tema en la lista TEMAS por su id.
    Retorna el diccionario del tema o None si no existe.
    """
    for tema in temas:
        if tema["id_tema"] == id_tema:
            return tema
    return None