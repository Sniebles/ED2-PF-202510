def calcular_total(cantidad, precio_unitario, descuento):
    """
    Calcula el total de una venta aplicando el descuento.

    Parámetros:
    cantidad (int): número de unidades vendidas.
    precio_unitario (float): precio por unidad.
    descuento (float): porcentaje de descuento aplicado.

    Retorna:
    float: valor total de la venta con descuento.
    """
    return cantidad * precio_unitario * (1 - descuento / 100)

calcular_total