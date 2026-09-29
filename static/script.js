document.addEventListener("DOMContentLoaded", function () {

    const modoEscuro = document.getElementById("modoEscuro");

    const temaSalvo = localStorage.getItem("tema");


    /*
     * Aplica o estado salvo do modo escuro
     */

    if (temaSalvo === "escuro") {

        document.documentElement.classList.add("modo-escuro");

        if (modoEscuro) {
            modoEscuro.checked = true;
        }

    } else {

        document.documentElement.classList.remove("modo-escuro");

        if (modoEscuro) {
            modoEscuro.checked = false;
        }

    }


    /*
     * Alterna o modo escuro
     */

    if (modoEscuro) {

        modoEscuro.addEventListener("change", function () {

            if (modoEscuro.checked) {

                document.documentElement.classList.add(
                    "modo-escuro"
                );

                localStorage.setItem(
                    "tema",
                    "escuro"
                );

            } else {

                document.documentElement.classList.remove(
                    "modo-escuro"
                );

                localStorage.setItem(
                    "tema",
                    "claro"
                );

            }

        });

    }

});