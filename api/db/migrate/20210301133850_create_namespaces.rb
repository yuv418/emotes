class CreateNamespaces < ActiveRecord::Migration[6.1]
  def change
    create_table :namespaces do |t|
      t.string :slug
      t.references :user, null: false, foreign_key: true

      t.timestamps
    end
  end
end
