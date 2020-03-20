window.addEventListener('load', (event) => {
    document.getElementById("id_ability_to_consent").addEventListener('change', function() {
        if(document.getElementById('id_ability_to_consent').value == 1) {
            document.getElementById('id_inability_reason').disabled = true;
            document.getElementById('id_representative_name').disabled = true;
            document.getElementById('id_relationship_to_patient').disabled = true;
            document.getElementById('id_relationship_to_patient').value = "";
        }
        else{
            document.getElementById('id_inability_reason').disabled = false;
            document.getElementById('id_representative_name').disabled = false;
            document.getElementById('id_relationship_to_patient').disabled = false;
        }});
});