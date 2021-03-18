class AddGlobalNamespace < ActiveRecord::Migration[6.1]
  def change
    global = Namespace.create(slug: "global", global: true)
  end
end
