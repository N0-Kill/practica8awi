app.service("decoracionesService", function ($http) {
    const urlBase = "https://practica8awi.onrender.com/Decoraciones"; // Ajusta la URL según tu API

    this.obtenerDecoraciones = function () {
        return $http.get(urlBase);
    };

    this.obtenerDecoracionPorId = function (id) {
        return $http.get(`${urlBase}/${id}`);
    };

    this.agregarDecoracion = function (decoracion) {
        return $http.post(urlBase, decoracion);
    };

    this.modificarDecoracion = function (id, decoracion) {
        return $http.put(`${urlBase}/${id}`, decoracion);
    };

    this.eliminarDecoracion = function (id) {
        return $http.delete(`${urlBase}/${id}`);
    };
});
