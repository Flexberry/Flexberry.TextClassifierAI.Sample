import {
  defineNamespace,
  defineProjections,
  Model as ReportMixin
} from '../mixins/regenerated/models/i-i-s-reports-text-classifier-ai-report';

import EmberFlexberryDataModel from 'ember-flexberry-data/models/model';

let Model = EmberFlexberryDataModel.extend(ReportMixin, {
});

defineNamespace(Model);
defineProjections(Model);

export default Model;
