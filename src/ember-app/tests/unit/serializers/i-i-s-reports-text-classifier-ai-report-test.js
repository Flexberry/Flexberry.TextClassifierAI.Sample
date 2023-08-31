import { moduleForModel, test } from 'ember-qunit';

moduleForModel('i-i-s-reports-text-classifier-ai-report', 'Unit | Serializer | i-i-s-reports-text-classifier-ai-report', {
  // Specify the other units that are required for this test.
  needs: [
    'serializer:i-i-s-reports-text-classifier-ai-report',
    'service:syncer',
    'transform:file',
    'transform:decimal',
    'transform:guid',

    'model:i-i-s-reports-text-classifier-ai-report-type',
    'model:i-i-s-reports-text-classifier-ai-report',
    'validator:ds-error',
    'validator:presence',
    'validator:number',
    'validator:date',
    'validator:belongs-to',
    'validator:has-many',
  ],
});

// Replace this with your real tests.
test('it serializes records', function(assert) {
  let record = this.subject();

  let serializedRecord = record.serialize();

  assert.ok(serializedRecord);
});
