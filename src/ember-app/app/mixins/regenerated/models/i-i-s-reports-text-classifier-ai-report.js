import Mixin from '@ember/object/mixin';
import $ from 'jquery';
import DS from 'ember-data';
import { validator } from 'ember-cp-validations';
import { attr, belongsTo, hasMany } from 'ember-flexberry-data/utils/attributes';

export let Model = Mixin.create({
  reportFile: DS.attr('file'),
  reportType: DS.belongsTo('i-i-s-reports-text-classifier-ai-report-type', { inverse: null, async: false })
});

export let ValidationRules = {
  reportFile: {
    descriptionKey: 'models.i-i-s-reports-text-classifier-ai-report.validations.reportFile.__caption__',
    validators: [
      validator('ds-error'),
    ],
  },
  reportType: {
    descriptionKey: 'models.i-i-s-reports-text-classifier-ai-report.validations.reportType.__caption__',
    validators: [
      validator('ds-error'),
    ],
  },
};

export let defineProjections = function (modelClass) {
  modelClass.defineProjection('ReportE', 'i-i-s-reports-text-classifier-ai-report', {
    reportFile: attr('Report file', { index: 0 }),
    reportType: belongsTo('i-i-s-reports-text-classifier-ai-report-type', '', {
      name: attr('', { index: 0 }),
      typeId: attr('', { index: 1 })
    }, { index: 1 })
  });

  modelClass.defineProjection('ReportL', 'i-i-s-reports-text-classifier-ai-report', {
    reportFile: attr('Report file', { index: 0 }),
    reportType: belongsTo('i-i-s-reports-text-classifier-ai-report-type', '', {
      typeId: attr('Type ID', { index: 0 })
    }, { index: -1, hidden: true })
  });
};
