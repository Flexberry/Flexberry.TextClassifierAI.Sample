import Mixin from '@ember/object/mixin';
import $ from 'jquery';
import DS from 'ember-data';
import { validator } from 'ember-cp-validations';
import { attr, belongsTo, hasMany } from 'ember-flexberry-data/utils/attributes';

export let Model = Mixin.create({
  name: DS.attr('string'),
  typeId: DS.attr('string')
});

export let ValidationRules = {
  name: {
    descriptionKey: 'models.i-i-s-reports-text-classifier-ai-report-type.validations.name.__caption__',
    validators: [
      validator('ds-error'),
    ],
  },
  typeId: {
    descriptionKey: 'models.i-i-s-reports-text-classifier-ai-report-type.validations.typeId.__caption__',
    validators: [
      validator('ds-error'),
    ],
  },
};

export let defineProjections = function (modelClass) {
  modelClass.defineProjection('ReportTypeE', 'i-i-s-reports-text-classifier-ai-report-type', {
    name: attr('', { index: 0 }),
    typeId: attr('', { index: 1 })
  });

  modelClass.defineProjection('ReportTypeL', 'i-i-s-reports-text-classifier-ai-report-type', {
    name: attr('', { index: 0 }),
    typeId: attr('', { index: 1 })
  });
};
