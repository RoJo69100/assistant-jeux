-- Renommage « soir » en « aujourd'hui » : public.rafraichir_avant_soir() devient public.rafraichir_avant_aujourdhui().
-- Les droits (service_role, assistant_ro) et le corps de la fonction (019) suivent le renommage.
-- Appliquée via le connecteur Supabase (migration rafraichir_avant_aujourdhui).

alter function public.rafraichir_avant_soir() rename to rafraichir_avant_aujourdhui;
