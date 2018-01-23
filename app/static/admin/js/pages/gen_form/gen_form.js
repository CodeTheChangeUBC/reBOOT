 // function upload(event) {
 //        event.preventDefault();
 //
 //        var data = new FormData($('#csv_form')[0]);
 //        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
 //        console.log(data);
 //
 //        function csrfSafeMethod(method) {
 //            // these HTTP methods do not require CSRF protection
 //            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
 //        }
 //
 //        $.ajaxSetup({
 //            beforeSend: function(xhr, settings) {
 //                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
 //                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
 //                }
 //            }
 //        });
 //
 //        $.ajax({
 //            url: $(this).attr('action'),
 //            type: $(this).attr('method'),
 //            enctype: $(this).attr('enctype'),
 //            data: data,
 //            cache: false,
 //            processData: false,
 //            contentType: false,
 //            success: function(data) {
 //                alert('success');
 //            },
 //            error: function(e) {
 //                console.log(e.message);
 //            }
 //        });
 //
 //        alert('Your file has been submitted. Please wait');
 //        return false;
 //    }
 //
 //    $(function() {
 //        $('#csv_form').submit(upload);
 //    });



//  const app = new Vue({
//     el: '#app',
//     data: {
//       editFriend: null,
//       friends: [],
//     },
//     methods: {
//       deleteFriend(id, i) {
//         fetch("http://rest.learncode.academy/api/vue-5/friends/" + id, {
//           method: "DELETE"
//         })
//         .then(() => {
//           this.friends.splice(i, 1);
//         })
//       },
//       updateFriend(friend) {
//         fetch("http://rest.learncode.academy/api/vue-5/friends/" + friend.id, {
//           body: JSON.stringify(friend),
//           method: "PUT",
//           headers: {
//             "Content-Type": "application/json",
//           },
//         })
//         .then(() => {
//           this.editFriend = null;
//         })
//       }
//     },
//     mounted() {
//       fetch("http://rest.learncode.academy/api/vue-5/friends")
//         .then(response => response.json())
//         .then((data) => {
//           this.friends = data;
//         })
//     },
//     template: `
//     <div>
//       <li v-for="friend, i in friends">
//         <div v-if="editFriend === friend.id">
//           <input v-on:keyup.13="updateFriend(friend)" v-model="friend.name" />
//           <button v-on:click="updateFriend(friend)">save</button>
//         </div>
//         <div v-else>
//           <button v-on:click="editFriend = friend.id">edit</button>
//           <button v-on:click="deleteFriend(friend.id, i)">x</button>
//           {{friend.name}}
//         </div>
//       </li>
//     </div>
//     `,
// });
var gen_form = new Vue({
    el: "#gen_form",

    components: {
        "vue-form-generator": VueFormGenerator.component
    },

    data() {
			return {
        model: {
            id: 1,
            name: "John Doe",
            password: "J0hnD03!x4",
						age: 35,
            skills: ["Javascript", "VueJS"],
            email: "john.doe@gmail.com",
            status: true
        },
        schema: {
            fields: [{
                type: "input",
								inputType: "text",
                label: "ID",
                model: "id",
                readonly: true,
                featured: false,
                disabled: true
            }, {
                type: "input",
								inputType: "text",
                label: "Name",
                model: "name",
                readonly: false,
                featured: true,
                required: true,
                disabled: false,
                placeholder: "User's name",
                validator: VueFormGenerator.validators.string
            }, {
                type: "input",
								inputType: "password",
                label: "Password",
                model: "password",
                min: 6,
                required: true,
                hint: "Minimum 6 characters",
                validator: VueFormGenerator.validators.string
            }, {
                type: "input",
                inputType: "number",
                label: "Age",
                model: "age",
								min: 18,
                validator: VueFormGenerator.validators.number
            }, {
                type: "input",
								inputType: "email",
                label: "E-mail",
                model: "email",
                placeholder: "User's e-mail address",
                validator: VueFormGenerator.validators.email
            }, {
                type: "checklist",
                label: "Skills",
                model: "skills",
                multi: true,
                required: true,
                multiSelect: true,
                values: ["HTML5", "Javascript", "CSS3", "CoffeeScript", "AngularJS", "ReactJS", "VueJS"]
            }, {
               type: "switch",
                label: "Status",
                model: "status",
                multi: true,
                readonly: false,
                featured: false,
                disabled: false,
                default: true,
								textOn: "Active",
								textOff: "Inactive"
            }]
        },

        formOptions: {
            validateAfterLoad: true,
            validateAfterChanged: true
        }
			};
    },

    methods: {
        prettyJSON: function(json) {
            if (json) {
                json = JSON.stringify(json, undefined, 4);
                json = json.replace(/&/g, '&').replace(/</g, '<').replace(/>/g, '>');
                return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function(match) {
                    var cls = 'number';
                    if (/^"/.test(match)) {
                        if (/:$/.test(match)) {
                            cls = 'key';
                        } else {
                            cls = 'string';
                        }
                    } else if (/true|false/.test(match)) {
                        cls = 'boolean';
                    } else if (/null/.test(match)) {
                        cls = 'null';
                    }
                    return '<span class="' + cls + '">' + match + '</span>';
                });
            }
        }
    },

});