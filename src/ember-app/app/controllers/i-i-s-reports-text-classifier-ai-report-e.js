import EditFormController from 'ember-flexberry/controllers/edit-form';
import { get, set } from '@ember/object';

export default EditFormController.extend({
  parentRoute: 'i-i-s-reports-text-classifier-ai-report-l',
  
  save: function(close) {
    let self = this;

    this._super(...arguments).then(function() {
      if (!close) {
        const modelId = get(self, 'model.id');
        const modelProj = get(self, 'modelProjection');
        const store = get(self, 'store');
        const findRecordParameters = { reload: true, projection: modelProj.projectionName }; 

        store.findRecord(modelProj.modelName, modelId, findRecordParameters)
          .then(function(modelAfterSaveRefreshed) {
          set(self, 'model', modelAfterSaveRefreshed);
        });
      }
    });
  },
});
