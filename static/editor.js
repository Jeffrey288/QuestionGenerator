var formSubmitting = false;

$(function () {

    const preview = document.querySelector('#preview')
    var editor = ace.edit("editor");
    console.log(editor)
    var converter = new showdown.Converter();
    editor.setOptions({ wrap: true });
    editor.setTheme("ace/theme/monokai");
    editor.session.setMode("ace/mode/html");
    preview.innerHTML = converter.makeHtml(editor.getValue());
    editor.session.on('change', function (delta) {
        preview.innerHTML = converter.makeHtml(editor.getValue());
        // delta.start, delta.end, delta.lines, delta.action
    });

    editor.commands.addCommand({
        bindKey: {
            win: 'Ctrl-L',
            mac: 'Command-L'
        },
        exec: function (editor) {
            editor.selection.selectLine();
        },
        readOnly: false // false if this command should not apply in readOnly mode
    });
    editor.commands.addCommand({
        bindKey: {
            win: 'Ctrl-D',
            mac: 'Command-D'
        },
        exec: function (editor) {
            if (editor.getSelectedText() != "") {
                editor.selectMore(1)
            } else {
                editor.toggleWord()
            }
        },
        readOnly: false
    });
    editor.commands.removeCommand(editor.commands.commands.removeline)



    /**
     * Actually unnecessary,
     * just for testing the upload file button
     */
    upload_input = document.querySelector("#upload")
    upload_input.addEventListener("change", function () {
        if (this.files.length) {
            var file = this.files[0];
            console.log(file.name, file.type)
        }
    });

    /**
     * Deals with pasting images into the editor
     */
    // https://stackoverflow.com/questions/166221/how-can-i-upload-files-asynchronously-with-jquery
    // https://gist.github.com/kidatti/f93feba1ec4be2117d1b

    /**
     * References:
     * 
     * [editor.onPaste.toString()]
     * function (e, t) {
     *     var n = { text: e, event: t };
     *     this.commands.exec("paste", this, n);
     * }
     * 
     * Event dispatch order (official documentation)
     * https://www.w3.org/TR/uievents/#event-flow
     * Event order (QnA)
     * https://www.quirksmode.org/js/events_order.html#link4
     * 
     * Disable ACE editor paste function
     * https://stackoverflow.com/questions/42951915/how-to-disable-paste-in-cloud9-ace-code-editor
     * 
     * Access ACE commands
     * https://stackoverflow.com/questions/59998538/cut-and-paste-in-ace-editor
     * 
     * Method one of accessing clipboard data: clipboard event
     * somehwere over the rainbow
     * 
     * Method two of accessing clipboard data: navigator clipboard API
     * - Clipboard ask for permission using promises
     *   https://ourcodeworld.com/articles/read/1567/how-to-cut-copy-paste-and-select-all-text-in-ace-editor
     *   https://developer.mozilla.org/en-US/docs/Web/API/Clipboard/read
     * 
     * Some other fragmented documentation about the editor:
     * https://stackoverflow.com/questions/23996814/how-can-i-get-selected-text-in-ace-editor
     * https://stackoverflow.com/questions/26555492/ace-editor-find-text-select-row-and-replace-text
     * 
     */

    const onPaste = function (event) {
        event.stopPropagation(); // stop capturing and bubbling
        event.preventDefault();

        // delete text in selection
        editor.session.replace(editor.selection.getRange(), "");

        // Method 1 is employed, and is way better
        var items = (event.clipboardData || event.originalEvent.clipboardData).items;
        for (var i = 0; i < items.length; i++) {
            var item = items[i];
            console.log(item)
            if (item.type.indexOf("image") != -1) {
                var file = item.getAsFile();
                img_link = upload_img_clipboard(file);
                editor.session.insert(editor.getCursorPosition(),
                    `<center><img src="/static/assets/projects/${img_link}" width="700px"  height='500px' style="object-fit:contain;"></center>`);
                console.log(img_link)
            } else if (item.type == 'text/plain') {
                item.getAsString(
                    (text) => { editor.session.insert(editor.getCursorPosition(), text); }
                );
            }
        }

    }
    document.querySelector(".ace_editor").addEventListener("paste", onPaste, true);

    /**
     * Does two things
     * 1. sends a POST request upon pressing the submit button
     * 2. redirects the user to the created/edited project page
     */
    function post() {
        if ($('#title').val() == '') {
            alert('Project Title is required!');
            return;
        }

        // Uses vanilla xhr to send POST request.
        // https://stackoverflow.com/questions/199099/how-to-manage-a-redirect-request-after-a-jquery-ajax-call
        const req = new XMLHttpRequest();
        var form_data = new FormData(); // uses FormData to store form data.
        var data = {
            'title': $('#title').val(),
            'desc': $('#desc').val(),
            'date': $('#date').val(),
            'tags': $('#tags').val(),
            'icon': $('#icon').val(),
            'content': editor.getValue()
        };
        for (var key in data) {
            form_data.append(key, data[key]);
        }
        console.log(window.location.pathname)
        req.open("POST", window.location.pathname, true);
        // req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        req.onreadystatechange = function () {
            if (req.readyState === 4) {
                formSubmitting = true;
                location.href = req.responseURL;
                // console.log(req.status);
                // console.log(req.responseURL);
            }
        };
        req.send(form_data);

    }
    document.querySelector("#submit").addEventListener('click', post);

    // ADAPTED FROM https://stackoverflow.com/questions/50735181/insert-markdown-for-bold-and-italics-around-selection

    document.querySelector(".ace_editor").addEventListener('keydown', function (e) {
        if (e.ctrlKey && $.inArray(e.keyCode, [66, 73, 85, 76, 68]) > -1) {
            console.log(editor)
            var keyCode = e.keyCode;
            var focused = document.querySelector("textarea");
            var id = focused.id;
            e.preventDefault();
            if (keyCode == 66) {
                insertFormating("**");
            } else if (keyCode == 73) {
                insertFormating("_");
            }
        }
    });

    function insertFormating(formatter) {
        // range: {start: ..., end: ...}
        // pos: {row: ..., column: ...}
        const range = editor.selection.getRange();
        const start = range.start;
        const end = range.end;
        if (editor.getSelectedText() == "") {
            editor.session.insert(start, formatter + formatter);
            var newPos = { row: start.row, column: start.column + formatter.length }
            // editor.selection.setSelectionRange({start: newPos, end: newPos}, false);
            editor.moveCursorToPosition(newPos)
            editor.clearSelection();
        } else {
            editor.session.replace(
                editor.selection.getRange(),
                formatter + editor.getSelectedText().trim() + formatter
            );
        }
    }

})

function upload_img_clipboard(file) {
    // https://developer.mozilla.org/en-US/docs/Web/API/FormData/Using_FormData_Objects
    formData = new FormData();
    formData.append("file", file)
    var xhr = $.ajax({
        url: '/upload',
        type: 'POST',
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        async: false,
    })
    // prompt('Image pasted. The following is the tag to the image: ', 
    //     `<img src="/static/assets/projects/${xhr.responseText}" width="700px"  height='700px' style="object-fit:contain;">`)
    return xhr.responseText;
}

/**
 * Uploads icon for the project and receives the name of the uploaded file.
 * @returns 
 */
function upload_img() {
    if (upload_input.files.length) {
        // https://developer.mozilla.org/en-US/docs/Web/API/FormData/Using_FormData_Objects
        formData = new FormData();
        formData.append("file", upload_input.files[0])
        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            success: function (data) {
                document.querySelector("#icon").setAttribute("value", data);
            }
        })
    } else {
        alert("Please select a file!");
    }
}

/**
 * Failed POST code (left here for reference)
 * 
 * 
    // var xhr = $.ajax({
    //     method: "POST",
    //     url: '/project-editor',
    //     data: {
    //         'title': $('#title').val(),
    //         'desc': $('#desc').val(),
    //         'date': $('#date').val(),
    //         'tags': $('#tags').val(),
    //         'icon': $('#icon').val(),
    //         'content': editor.getValue()
    //     },
    //     success: function (data, textStatus, request) {
    //         console.log(xhr.getAllResponseHeaders())
    //         console.log("hey")
    //     },
    //     error: function(jqXHR, textStatus, errorThrown) {}
    // })

    // var xhr = $.post('/project-editor', {
    //     'title': $('#title').val(),
    //     'desc': $('#desc').val(),
    //     'date': $('#date').val(),
    //     'tags': $('#tags').val(),
    //     'icon': $('#icon').val(),
    //     'content': editor.getValue()
    // }, function (data) {
    //     console.log(data)
    //     document.querySelector('html').innerHTML = data;
    //     console.log("wah")
    // });
    // console.log(xhr);
 */

// Prevent unsaved changes:
// https://stackoverflow.com/questions/7317273/warn-user-before-leaving-web-page-with-unsaved-changes

// window.onload = function () {
//     window.addEventListener("beforeunload", function (e) {
//         if (formSubmitting) {
//             return undefined;
//         }

//         var confirmationMessage = 'It looks like you have been editing something. '
//             + 'If you leave before saving, your changes will be lost.';

//         (e || window.event).returnValue = confirmationMessage; //Gecko + IE
//         return confirmationMessage; //Gecko + Webkit, Safari, Chrome etc.
//     });
// };
