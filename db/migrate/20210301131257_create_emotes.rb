class CreateEmotes < ActiveRecord::Migration[6.1]
  def change
    create_table :emotes do |t|
      t.string :name
      t.integer :emote_type
      t.string :slug

      t.timestamps
    end
  end
end
