from src.utils import validar_id_usuario


def test_validar_id_usuario():
    # Arrange
    id_usuario = "10"
    # Act
    resultado = validar_id_usuario(id_usuario)
    # Assert
    assert resultado == True
