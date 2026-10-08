from src.datos import temas
import src.services as services
import src.interface as interface

def main():
    id_tema = interface.get_id_tema() 
    result = services.buscar_tema_por_id(int(id_tema), temas)
    print(f"Resultado de la búsqueda: {result}")


# ============================================================
if __name__ == "__main__":
    main()
