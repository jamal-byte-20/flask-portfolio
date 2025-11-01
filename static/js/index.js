
addEventListener('DOMContentLoaded',()=>{
    let s0 = document.querySelector("#s0");
    let s1 = document.querySelector("#s1");
    s0?.classList?.add("s0");
    s1?.classList?.add("s1");
})
state = false;
let btn_menu = document.querySelector("#menu")
let nav = document.querySelector("nav")

btn_menu.addEventListener('click',()=>{

    btn_menu.classList.toggle("ss");
    nav.classList.toggle("active");
    if(btn_menu.innerHTML == "☰"){
        btn_menu.innerHTML = "x";
    }else{
        btn_menu.innerHTML = "&#9776"
    }
},true)