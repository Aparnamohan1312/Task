from django.test import TestCase

class ValidationErrorTestMixin(object):

    @contextmanager
    def assertValidationErrors(self, fields):
        """
        Assert that a validation error is raised, containing all the specified
        fields, and only the specified fields.
        """
        try:
            yield
            raise AssertionError("ValidationError not raised")
        except ValidationError as e:
            self.assertEqual(set(fields), set(e.message_dict.keys()))
            class ModelFormBaseTest(TestCase):
    def test_base_form(self):
        self.assertEqual(list(BaseCategoryForm.base_fields), ['name', 'slug', 'url'])

    def test_no_model_class(self):
        class NoModelModelForm(forms.ModelForm):
            pass
        with self.assertRaisesMessage(ValueError, 'ModelForm has no model class specified.'):
            NoModelModelForm()

    def test_empty_fields_to_fields_for_model(self):
        """
        An argument of fields=() to fields_for_model should return an empty dictionary
        """
        field_dict = fields_for_model(Person, fields=())
        self.assertEqual(len(field_dict), 0)

    def test_empty_fields_on_modelform(self):
        """
        No fields on a ModelForm should actually result in no fields.
        """
        class EmptyPersonForm(forms.ModelForm):
            class Meta:
                model = Person
                fields = ()

        form = EmptyPersonForm()
        self.assertEqual(len(form.fields), 0)

    def test_empty_fields_to_construct_instance(self):
        """
        No fields should be set on a model instance if construct_instance receives fields=().
        """
        form = modelform_factory(Person, fields="__all__")({'name': 'John Doe'})
        self.assertTrue(form.is_valid())
        instance = construct_instance(form, Person(), fields=())
        self.assertEqual(instance.name, '')

    def test_blank_with_null_foreign_key_field(self):
        """
        #13776 -- ModelForm's with models having a FK set to null=False and
        required=False should be valid.
        """
        class FormForTestingIsValid(forms.ModelForm):
            class Meta:
                model = Student
                fields = '__all__'

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['character'].required = False
    
    def test_missing_fields_attribute(self):
        message = (
            "Creating a ModelForm without either the 'fields' attribute "
            "or the 'exclude' attribute is prohibited; form "
            "MissingFieldsForm needs updating."
        )
        with self.assertRaisesMessage(ImproperlyConfigured, message):
            class MissingFieldsForm(forms.ModelForm):
                class Meta:
                    model = Category

    def test_extra_fields(self):
        class ExtraFields(BaseCategoryForm):
            some_extra_field = forms.BooleanField()

        self.assertEqual(list(ExtraFields.base_fields),
                         ['name', 'slug', 'url', 'some_extra_field'])

    def test_extra_field_model_form(self):
        with self.assertRaisesMessage(FieldError, 'no-field'):
            class ExtraPersonForm(forms.ModelForm):
                """ ModelForm with an extra field """
                age = forms.IntegerField()

                class Meta:
                    model = Person
                    fields = ('name', 'no-field')

    def test_extra_declared_field_model_form(self):
        class ExtraPersonForm(forms.ModelForm):
            """ ModelForm with an extra field """
            age = forms.IntegerField()

            class Meta:
                model = Person
                fields = ('name', 'age')
