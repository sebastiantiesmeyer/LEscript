//list of all default languages and button memory:
var languages = ["Spanish",'Mandarin',
'Japanese','Russian','Bengali ','Portuguese','Arabic' ,
'Punjabi','German','French','Turkish','Italian','Polish',
'Greek','Swedish','Czech','Hungarian'];
languages.sort();
languages = ['English','Dutch'].concat(languages).concat(['other...']);

//Proficiency levels for teaching/learning languages;
var proficiencies = {'L': ['B','I','A'],
                  'T': ['A','N']};
var prof_written = {'L': ['beginner','interm.','advanced'],
                  'T': ['advanced','native']};
//stores all Learn/Teach buttons.
var buttonsL = [];
var buttonsT = [];


/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
// function expandDdn(e) {
//     var id = (e.target.id).replace("btn", "ddn");
//     document.getElementById(id).classList.toggle("show");
//   }
  
  // Close the dropdown menu if the user clicks outside of it
//   window.onclick = function(event) {
//     if (!event.target.matches('.dropbtn')) {
//       var dropdowns = document.getElementsByClassName("dropdown-content");
//       var i;
//       for (i = 0; i < dropdowns.length; i++) {
//         var openDropdown = dropdowns[i];
//         if (openDropdown.classList.contains('show')) {
//           openDropdown.classList.remove('show');
//         }
//       }
//     }
//   } 

//add a new dropdown menu to 'teach' (arg="T") or 'learn' (arg="L")
function add_ddn(learn){

    var id = "section"+learn;                     //find the correct section
    var div = document.getElementById(id);        
    var btn =document.createElement("select");   // Create a <button> element

    var btnId = ((learn == 'L') ?  "btn"+learn+((buttonsL.length).toString()) : "btn"+learn+((buttonsT.length).toString()));
    btn.setAttribute("id",btnId);

    btn.onchange= function(e){selectLanguage(e)};
    btn.setAttribute("class","dropbtn");
    btn.topmost = true

    var btnId = ((learn == 'L') ?  "btn"+learn+((buttonsL.length).toString()) : "btn"+learn+((buttonsT.length).toString()));
    btn.setAttribute("id",btnId);
    var p =document.createElement("p"); 

    var option = document.createElement('option');
    option.text = 'add language';
    option.selected = true;
    option.disabled = true;
    option.hidden = true;
    btn.add(option);

    for (var i=0;i<languages.length;i++){
        var option = document.createElement('option');
        option.text = languages[i];
        btn.add(option);
    }

    p.appendChild(btn);  


  
  var radios = document.createElement("div");
  radios.className = "radios";
  radios.id = "radios"+learn+((((learn == 'L') ?  buttonsL.length : buttonsT.length).toString()));
  
  var len = ((proficiencies[learn]).length);
    for (var i =0;i<len;i++){
      var radio = document.createElement('input');
      radio.setAttribute('type', 'radio');
      if (!i) {radio.setAttribute("checked","checked")};
    radio.setAttribute('name','prof'+learn+(((learn == 'L') ?  buttonsL : buttonsT).length).toString());
    radio.setAttribute('value',proficiencies[learn][i]);
    var label = document.createElement("label");
    label.setAttribute("for",radio.id);
    label.innerHTML = prof_written[learn][i];
    radios.appendChild(label);
    //radio.innerHTML(proficiencies[learn][i]);
    radios.appendChild(radio);
  }
  var inputBox = document.createElement('input');
  inputBox.setAttribute('type','text');
  inputBox.setAttribute('name','other'+learn+(((learn == 'L') ?  buttonsL : buttonsT).length).toString());
  inputBox.defaultValue='other language...';
//   fillContent(learn);

  p.appendChild(radios);
 
  p.appendChild(inputBox);
  div.appendChild(p);  
  (learn == 'L') ? buttonsL.push(btnId) : buttonsT.push(btnId);

}

// //fill all the options into the newly created dropdown menu:
// function fillContent(learn){
//     var id = "section"+learn;
//     var div = document.getElementById(id);
//     var ddn = document.createElement("div");
//     ddn.setAttribute("class","dropdown-content");
//     var ddnId = ((learn == 'L') ?  "ddn"+learn+((buttonsL.length).toString()) : "ddn"+learn+((buttonsT.length).toString()));
//     ddn.setAttribute("id",ddnId);
//     for (var i =0;i<languages.length;i++){
//         var a = document.createElement("a");

//         a.onclick= function(e){selectLanguage(e)};
//         a.innerHTML = languages[i];

//         ddn.appendChild(a);
//     }
//     div.appendChild(ddn);

// }

//listens to events from the language dropdown menu.
function selectLanguage(e){

    id = e.target.id;
    // alert(e.target.selectedOptions[0].value)
    var option = e.target.selectedOptions[0].value;

    if (e.target.topmost)
    {
        var learn = id[3];
         add_ddn(learn);
         e.target.topmost=false;
  };  
  if (option==="other..."){
    document.getElementsByName(id.replace("btn","other" ))[0].style.display = "inline";
  }
  else{
    document.getElementsByName(id.replace("btn","other" ))[0].style.display = "none";
  }
    document.getElementById(id.replace("btn","radios" )).style.display = "inline";
    // document.getElementById(id).innerHTML = e.target.innerHTML;    
    document.getElementById(id).style.backgroundColor = "rgb( 73,175, 55)";
}

function reset(){
    location.reload(); 
}

function submit(){
    var XHR = new XMLHttpRequest();  
  var list = ((document.getElementsByClassName("headerbox")));
  if (!list[2].value.includes("@")){
    alert("Please enter a valid e-mail address!");
    return;
  }
  var data = [];
  for (let item of list){
    if (item.value === ""){
      alert("Please fill out your personal contact information.");
      return;
    }
    else{
      data.push(item.value)
    }
  }    
  data.push('L:');
  if (buttonsL.length==1){
    alert("Please select at least one language to practice.");
    return;
  };

  var text="";
  for (let item of buttonsL){
    text = (document.getElementById(item).selectedOptions[0].value);
    if (text==="add language"){
      break;
    }
    else if (text==="other..."){
      var textId = item.replace("btn","other");
      var value = (document.getElementsByName(textId)[0].value);
      switch (value){
        case "":{
          alert ("Please fill in your 'other' language.");
        return;}
        case "other language plz :)":{
          alert ("Please fill in your 'other' language.");
        return;}
      default:{
        data.push(value);
      }
      }
    }
    else {
      data.push(text);
    }
    data.push(document.getElementsByName(item.replace('btn','prof'))[0].value);

  }


  if (buttonsT.length==1){
    alert("Please select at least one language to teach.");
    return;
  };
  data.push('T:');

  for (let item of buttonsT){
    text = (document.getElementById(item).selectedOptions[0].value);
    if (text==="add language"){
      break;
    }
    else if (text==="other..."){
      var textId = item.replace("btn","other");
      var value = (document.getElementsByName(textId)[0].value);
      switch (value){
        case "":{
          alert ("Please fill in your 'other' language.");
        return;}
        case "other language...":{
          alert ("Please fill in your 'other' language.");
        return;}
      default:{
        data.push(value);
      }
      }
    }
    else {
      data.push(text);
    }
    data.push(document.getElementsByName(item.replace('btn','prof'))[0].value);

  }
  // Define what happens on successful data submission
  XHR.addEventListener('load', function(event) {
    alert('Yeah! Data sent and response loaded.');
  });

  // Define what happens in case of error
  XHR.addEventListener('error', function(event) {
    alert('Oops! Something went wrong.');
  });

  XHR.open('POST', 'http://127.0.0.1:5000/');
  XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

  XHR.send(data);
//   alert(data);
}
