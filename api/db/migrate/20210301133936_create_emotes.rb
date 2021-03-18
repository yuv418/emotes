class CreateEmotes < ActiveRecord::Migration[6.1]
  def change
    create_table :emotes do |t|
      t.string :name
      t.integer :emote_type
      t.string :slug
      t.references :namespace, null: false, foreign_key: true

      t.timestamps
    end
  end
end
