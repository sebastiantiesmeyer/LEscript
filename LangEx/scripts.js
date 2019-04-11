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
function expandDdn(e) {
    var id = (e.target.id).replace("btn", "ddn");
    document.getElementById(id).classList.toggle("show");
  }
  
  // Close the dropdown menu if the user clicks outside of it
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  } 

//add a new dropdown menu to 'teach' (arg="T") or 'learn' (arg="L")
function add_ddn(learn){

  var id = "section"+learn;                     //find the correct section
  var div = document.getElementById(id);        
  var btn =document.createElement("BUTTON");   // Create a <button> element
  btn.innerHTML = "add language";                   // Insert text
  btn.onclick= function(e){expandDdn(e)};
  btn.setAttribute("class","dropbtn");
  var btnId = ((learn == 'L') ?  "btn"+learn+((buttonsL.length).toString()) : "btn"+learn+((buttonsT.length).toString()));
  btn.setAttribute("id",btnId);
  var p =document.createElement("p");   

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
  inputBox.defaultValue='other language plz :)';
  fillContent(learn);

  p.appendChild(radios);
 
  p.appendChild(inputBox);
  div.appendChild(p);  
  (learn == 'L') ? buttonsL.push(btnId) : buttonsT.push(btnId);

}

//fill all the options into the newly created dropdown menu:
function fillContent(learn){
    var id = "section"+learn;
    var div = document.getElementById(id);
    var ddn = document.createElement("div");
    ddn.setAttribute("class","dropdown-content");
    var ddnId = ((learn == 'L') ?  "ddn"+learn+((buttonsL.length).toString()) : "ddn"+learn+((buttonsT.length).toString()));
    ddn.setAttribute("id",ddnId);
    for (var i =0;i<languages.length;i++){
        var a = document.createElement("a");

        a.onclick= function(e){selectLanguage(e)};
        a.innerHTML = languages[i];

        ddn.appendChild(a);
    }
    div.appendChild(ddn);

}

//listens to events from the language dropdown menu.
function selectLanguage(e){
    id = e.target.parentNode.id.replace("ddn", "btn");
    if (document.getElementById(id).innerHTML==="add language"){
      var learn = id[3];
      add_ddn(learn)
  };  
  if (e.target.innerHTML==="other..."){
    document.getElementsByName(id.replace("btn","other" ))[0].style.display = "inline";
  }
  else{
    document.getElementsByName(id.replace("btn","other" ))[0].style.display = "none";
  }
    document.getElementById(id.replace("btn","radios" )).style.display = "inline";
    document.getElementById(id).innerHTML = e.target.innerHTML;    
    document.getElementById(id).style.backgroundColor = "rgb( 73,175, 55)";
}

function submit(){
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
  if (buttonsL.length==0){
    alert("Please select at least one language to practice.");
    return;
  };

  var text="";
  for (let item of buttonsL){
    text = (document.getElementById(item).innerHTML);
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


  if (buttonsT.length==0){
    alert("Please select at least one language to teach.");
    return;
  };
  data.push('T:');

  for (let item of buttonsT){
    text = (document.getElementById(item).innerHTML);
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
  alert(data.join(';;;'));
  

}
