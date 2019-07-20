function addRoles() {
      document.getElementById("myForm").style.display = "block";
    }

    function closeForm() {
      document.getElementById("myForm").style.display = "none";
    }
        $('#parentterriority').ready(function(){
          $.ajax({
                    url: "/accounts/territory/",
                    type: "GET",
                    contentType: false,
                    processData:false,
                    success: function(data)
                    {
                        json = JSON.parse(data)  
                        var html = '' 
                        html += '<select name="parentterriority" id="parentterriority" class="form-container">'+
                                '<option value="">select</option>';
                        for(i=0;i<json.length;i++){
                            html += '<option value="' + json[i]['fields']['roles']+ '">'+json[i]['fields']['roles']+'</option>';
                        }        
                        html += '</select>';
                        $('#select_box').html(html);
                    },
                    error: function() 
                    {

                    }           
            });
        });