
$(document).ready(function(){
    $("#btnVer").click(function(){
        $.get("https://fakestoreapi.com/products",
        function(data) {
            $.each(data,
                function(i, item){
                    var fila = `
                            <tr vertical-align="middle" style="border: 1px solid black;">
                                <td style="border: 1px black" class="col-lg-2">
                                    <img src="${item.image}"  style="width: 100px" &nbsp&nbsp>
                                </td>
                                <td style="border: 1px black" class="col-lg-3">
                                    ${item.title}
                                </td>
                                <td style="border: 1px black" class="col-lg-4">
                                    ${item.description}
                                </td>
                            </tr>
                        `;
                    $("#rifa").append(fila);
                });
            });        
    });
});