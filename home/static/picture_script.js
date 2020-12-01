function pasteHandler(e) {
    if (e.clipboardData) {
       // Get the items from the clipboard
       var items = e.clipboardData.items;
       if (items) {
          // Loop through all items, looking for any kind of image
          for (var i = 0; i < items.length; i++) {
             if (items[i].type.indexOf("image") !== -1) {
                // We need to represent the image as a file,
                var blob = items[i].getAsFile();
                var URLObj = window.URL || window.webkitURL;
                var source = URLObj.createObjectURL(blob);
                var reader = new FileReader();
                reader.onload = function(e) {
                  document.getElementById("summaryImage").value= reader.result;
                }
                reader.readAsDataURL(blob);
             } 
           }
       }
    } 
 }