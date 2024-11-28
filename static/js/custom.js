
async function rater(pid,uid){
    var review= document.getElementById("review")
    var rate= document.getElementById("rate")
    if((review.value.length!=0)&&(rate.value>0)&&(rate.value<6)){
        var responce=await fetch("/rateing/",{
            method:"POST",
            body: JSON.stringify({
                pid:pid,
                uid:uid,
                review:review.value,
                star:rate.value,
    
            }),
            credentials: "same-origin",
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
    
        })
        var data= await responce.json()
        if(data.status==200){
            review.value=''
            rate.value=''
        }



    
    }else{
        alert("please write a proper review star must be 1 to 5 and not give blank review")
    }
        

   

    
    
}



async function addtocart(pid,uid){
    var noi= document.getElementById("inputQuantity")
    var atc= document.getElementById("atc")
    var box= document.querySelectorAll(".bi-cart-fill me-1")
    
    
    var responce=await fetch("/cart/add/",{
        method:"POST",
        body: JSON.stringify({
            noi:noi.value,
            pid:pid,
            uid:uid,
        }),
        credentials: "same-origin",
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }

    })
    var data= await responce.json()
    if(data.message==true){
        noi.disabled=true
        
        box[0].classList.add("fa-solid fa-check text-success")
        atc.innerText=' Added'

    }else{

    }



    
 
        

   

    
    
}

async function updatecart(ids,pid,uid){
    
    var noi= document.getElementById(uid+ids)
    var price = document.getElementById("p"+ids)
    
    
    
    var responce=await fetch("/cart/update/",{
        method:"POST",
        body: JSON.stringify({
            noi:Number(noi.value),
            pid:pid,
            ids:ids, 
            uid:uid,
        }),
        credentials: "same-origin",
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }

    })
    var data= await responce.json()
    console.log(data)
    if(data.status==200){
        console.log(data)
        price.innerText="$"+data.price
    }else{
    }   
    
}


async function deletecart(ele,ids){
    
    
    
    
    
    var responce=await fetch("/cart/delete/",{
        method:"POST",
        body: JSON.stringify({
            
            ids:ids, 
            
        }),
        credentials: "same-origin",
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }

    })
    var data= await responce.json()
    console.log(ele,data)
    if(data.status==200){
        ele.parentElement.remove()
    }else{
    }   
    
}