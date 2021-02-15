window.addEventListener('load', function() {
    const notification = document.getElementById('djhj-notification');

    let isDraggble = false;

    notification.querySelector('[name="close"]').addEventListener('click', function() {
        notification.remove();
    });

    dragElement(notification);

    function dragElement(elmnt) {
        var pos1 = 0, pos2 = 0;
        elmnt.onmousedown = dragMouseDown;
        elmnt.onmouseup = closeDragElement;

        function dragMouseDown(e) {
            e = e || window.event;

            if (event.target.hasAttribute('name')) return;

            e.preventDefault();
            pos2 = e.clientX;
            document.onmouseup = closeDragElement;
            document.onmousemove = elementDrag;
        }

        function elementDrag(e) {
            e = e || window.event;
            e.preventDefault();
            pos1 = pos2 - e.clientX;
            pos2 = e.clientX;

            notification.classList.add('_draggble');

            function getTranslateX(myElement) {
                var style = window.getComputedStyle(myElement);
                var matrix = new WebKitCSSMatrix(style.transform);
                return matrix.m41;
            }

            elmnt.style.transform = 'translateX(' + (getTranslateX(elmnt) - pos1) + 'px)';
        }

        function closeDragElement() {
            document.onmouseup = null;
            document.onmousemove = null;
            notification.classList.remove('_draggble');
        }
    }
});
