function mostrarSideBar() {
    document.querySelector(".side-bar").classList.add("ativa");
}

function esconderSideBar() {
    document.querySelector(".side-bar").classList.remove("ativa");
}

function abrirMenuEditarCliente() {
    document.querySelector(".mini-menu").classList.add("ativa");
}

function esconderMenuEditarCliente() {
    document.querySelector(".mini-menu").classList.remove("ativa");
}

function scrollAteContatos() {
    const linkContatos = document.getElementById("link-contatos");

    if (linkContatos) {
        linkContatos.addEventListener("click", function (event) {
            event.preventDefault();

            const contatosDiv = document.getElementById("contatos");

            if (contatosDiv) {
                contatosDiv.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });
            }
        });
    }
}
function scrollAteSobre(){
    const linkSobre = document.getElementById("Sobre")
    if(linkSobre){
        Event.preventDefault();
        if(sobreDiv){
            sobreDiv.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
        }
    }
}
scrollAteContatos();
function esconderX() {
    const popup = document.querySelector(".pop-up");
    if (popup) {
      popup.classList.add("esconder");
    }
}