import { Component, OnInit, Input, Directive } from '@angular/core';
import { User } from '../shared/user.model';
import { NgForm, Validator, AbstractControl, NG_VALIDATORS } from '@angular/forms';
import { UserService } from '../shared/user.service';
import { ToastrService } from 'ngx-toastr'

 
var rolelist = [{
  "id": 2, "name": "partner"
},
{ "id": 3, "name": "member" },
]
@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css'],
})
export class SignUpComponent implements OnInit {
  user: User;
  emailPattern = "^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$"
  constructor(private userService: UserService, private toastr: ToastrService) { }

  ngOnInit(): void {
    this.resetForm();
  }
  resetForm(form?: NgForm) {
    if (form != null)
    form.reset()
    this.user = {
    username: '',
    password: '',
    confirmpassword: '',    
    mobile: '',
    email: '',
    invitedbycode: '',
    rolename: '',
    roleid: ''
    }
  }
   
  roleAllFn(role) {
    this.user.roleid = role.id;
    this.user.rolename = role.name;
    console.log("role", role)
  }
  onSubmit(form: NgForm) {
    const finaldata = {
      username: this.user.username,
      password: this.user.password,
      email: this.user.email,
      mobile: this.user.mobile,
      userroleid: this.user.roleid,
      userrolename: this.user.rolename,
      invitedbycode: this.user.invitedbycode,
    }
    console.log(JSON.stringify(finaldata));
    this.userService.registerUser(form.value)
    .subscribe((data:any) => {
    if (data.Succeeded == true) {
      this.resetForm(form);
      this.toastr.success('User Registration Successful');
    }
    else {
      this.toastr.error(data.Errors[0]);
    }
    
    })
  }
}
@Directive({
  selector: '[appConfirmEqualValidator]',
  providers: [{
    provide: NG_VALIDATORS,
    useExisting: ConfirmEqualValidatorDirective,
    multi: true
  }]
})
export class ConfirmEqualValidatorDirective implements Validator {
  @Input() appConfirmEqualValidator: string;
  validate(control: AbstractControl): { [key: string]: any } | null {
    const controlToCompare = control.parent.get(this.appConfirmEqualValidator);
    if (controlToCompare && controlToCompare.value !== control.value) {
      return { 'notEqual': true };
  }
  return null;
}
}

