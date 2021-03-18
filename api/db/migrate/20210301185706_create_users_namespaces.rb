class CreateUsersNamespaces < ActiveRecord::Migration[6.1]
  def change
    create_table :namespaces_users do |t|
      t.references :namespace, null: false, foreign_key: true
      t.references :user, null: false, foreign_key: true

      t.timestamps
    end
  end
end
