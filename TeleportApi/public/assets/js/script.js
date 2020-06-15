window.onload=function(){
    var menuElem = document.getElementById('dropdown-menu'),
        titleElem = menuElem.querySelector('.dropdown_title');
        document.onclick = function(event) {
        var target = elem = event.target;
        while (target != this) {
                if (target == menuElem) {
                    if(elem.tagName == 'A') titleElem.innerHTML = elem.textContent;
                    menuElem.classList.toggle('open')
                        return;
                }
                target = target.parentNode;
        }
        menuElem.classList.remove('open');
    }

    
}