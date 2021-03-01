class AddGlobalToNamespace < ActiveRecord::Migration[6.1]
  def change
    add_column :namespaces, :global, :boolean, default: false, null: false
  end
end
