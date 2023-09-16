// google auto complete

// let autocomplete;

// function initAutoComplete(){
// autocomplete = new google.maps.places.Autocomplete(
//     document.getElementById('id_address'),
//     {
//         types: ['geocode', 'establishment'],
//         //default in this app is "IN" - add your country code
//         componentRestrictions: {'country': ['in']},
//     })
// // function to specify what should happen when the prediction is clicked
// autocomplete.addListener('place_changed', onPlaceChanged);
// }

// function onPlaceChanged (){
//     var place = autocomplete.getPlace();

//     // User did not select the prediction. Reset the input field or alert()
//     if (!place.geometry){
//         document.getElementById('id_address').placeholder = "Start typing...";
//     }
//     else{
//         console.log('place name=>', place.name)
//     }
//     // get the address components and assign them to the fields
//     var geocoder = new google.maps.Geocoder()
//     var address = documents.getElementById("id_address").value;
//     geocoder.geocode({'address': address}, function(results, status){
//         if (status === google.maps.GeocoderStatus.OK){
//             var latitude = results[0].geometry.location.lat();
//             var longitude = results[0].geometry.location.lng();

//             $('#id_latitude').val(latitude)
//             $('#id_longitude').val(longitude)
//             $('#id_address').val(address)
//         }
//     });
//     // loop through the address component and assign data 
//     for (var i = 0;i<place.address_components.length;i++){
//         for(var j = 0;j<place.address_components[i].types.length;j++){
//             // get country
//             if(place.address_components[i].types[j]=='country'){
//                 $("#id_country").val(place.address_components[i].long_name);
//             }
//             // get state
//             if(place.address_components[i].types[j]=='administrative_area_level_1'){
//                 $("#id_state").val(place.address_components[i].long_name);
            
//             }
//             // get city
//             if(place.address_components[i].types[j]=='locality'){
//                 $("#id_city").val(place.address_components[i].long_name);
            
//             }
//             // get zip code
//             if(place.address_components[i].types[j]=='postal_code'){
//                 $("#id_pincode").val(place.address_components[i].long_name);
//             }
//             else{
//                 $("#id_pincode").val("");
//             }
//         }
//     }

// }




// cart ajax 

$(document).ready(function(){
    // add to cart
    $('.add_to_cart').on('click',function(e){
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        
        $.ajax({
            type:'GET',
            url:url,
            
            success:function(response){
                if(response.status == 'login_required'){
                    swal(response.message,'','info').then(function(){
                        window.location = '/login';
                    })
                }
                else if(response.status == 'Failed'){
                     swal(response.message,'','error')
                }
                else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);
                    // subtotal tax and grandtotal 
                    applyCartAmounts(response.cart_ammount['subtotal'],response.cart_ammount['tax'],response.cart_ammount['grand_total']);
                    
                    

                }
                
            }
                
        })
                     
    })

    // place cart item quantity on load 
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty)
    
    })


    // decrease cart value 
    $('.decrease_cart').on('click',function(e){
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('id');

        $.ajax({
            type:'GET',
            url:url,
            
            success:function(response){
                
                if(response.status == 'login_required'){
                    swal(response.message,'','info').then(function(){
                        window.location = '/login';
                    })
                }
                else if(response.status == 'Failed'){
                     swal(response.message,'','error')
                }
                else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);
                    applyCartAmounts(response.cart_ammount['subtotal'],response.cart_ammount['tax'],response.cart_ammount['grand_total']);
                    if(window.location.pathname=='/cart/'){
                    removeCartItem(response.qty,cart_id);
                    checkEmptyCart();
                    }
                }
                
            }
                
        })
                     
    })
// delete cart 

$('.delete_cart').on('click',function(e){
        e.preventDefault();
        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        
        $.ajax({
            type:'GET',
            url:url,
            
            success:function(response){
                
               
                if(response.status == 'Failed'){
                     swal(response.message,'','error')
                }
                else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    swal(response.status,response.message,'success')
                    applyCartAmounts(response.cart_ammount['subtotal'],response.cart_ammount['tax'],response.cart_ammount['grand_total']);
                    removeCartItem(0,cart_id);
                    checkEmptyCart();
                }
                
            }
                
        })
                     
    })

    // delete cart item card
    function removeCartItem(cartItemQty,cart_id){
        if(window.location.pathname=='/cart/'){
            if(cartItemQty <=0){
                document.getElementById('cart-item-'+cart_id).remove()
            }
        }
    }
    function checkEmptyCart(){
        var cart_counter = document.getElementById('cart_counter').innerHTML;
        if (cart_counter == 0){
            document.getElementById('empty-cart').style.display = 'block';
        }
    }


    // apply cart ammounts 
    function applyCartAmounts(subtotal,tax,grand_total){
        if(window.location.pathname=='/cart/'){
            $('#subtotal').html(subtotal);
            $('#tax').html(tax);
            $('#total').html(grand_total);
        }
    }

});